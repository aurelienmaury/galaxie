#! /bin/bash
#Inspirate by : http://blog.bigdinosaur.org/securing-ssh-with-iptables/
#tcp        0      0 192.168.1.69:5060       0.0.0.0:*               LISTEN      2374/asterisk   
#tcp        0      0 192.168.1.69:80         0.0.0.0:*               LISTEN      29660/apache2   
#tcp        0      0 192.168.1.69:2000       0.0.0.0:*               LISTEN      2374/asterisk   
#tcp        0      0 192.168.1.69:465        0.0.0.0:*               LISTEN      2082/sslserver  
#tcp        0      0 127.0.0.1:53            0.0.0.0:*               LISTEN      2090/dnscache   
#tcp        0      0 192.168.1.69:21         0.0.0.0:*               LISTEN      2078/tcpserver  
#tcp        0      0 192.168.1.69:22         0.0.0.0:*               LISTEN      1977/sshd       
#tcp        0      0 192.168.1.69:25         0.0.0.0:*               LISTEN      2083/tcpserver  
#tcp        0      0 192.168.1.69:993        0.0.0.0:*               LISTEN      2088/tcpserver 

PORT_SSH=22
PORT_SMTP=25
PORT_SIP=5060
CHAIN_NAME_SSH=SSH_DENY
CHAIN_NAME_SMTP=SMTP_DENY
LOG_FILE=/var/log/iptables.log

#Allow all RELATED,ESTABLISHED session
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT 

#Here, the rule will be applied to packets that signal the start of new connections headed for TCP port 22.
#If a packet matches those attributes, iptables will note the remote host’s address in a temporary list.
iptables -A INPUT -p tcp -m tcp --dport $PORT_SSH  -m state --state NEW -m recent --set --name DEFAULT --rsource
iptables -A INPUT -p tcp -m tcp --dport $PORT_SMTP -m state --state NEW -m recent --set --name DEFAULT --rsource

#The second rule will actually perform an action using a different chain, and in order to append it, 
#we’ll need to first create the chain that it’s going to reference:
iptables -N $CHAIN_NAME_SSH
iptables -N $CHAIN_NAME_SMTP

#This rule tells iptables to look for packets that match the previous rule’s parameters,
#and which also come from hosts already added to the watch list. 
#If iptables sees a packet coming from such a host, it will update the “last seen” timestamp for that host
iptables -A INPUT  -p tcp -m tcp --dport $PORT_SSH  -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --name DEFAULT --rsource -j $CHAIN_NAME_SSH
iptables -A INPUT  -p tcp -m tcp --dport $PORT_SMTP -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --name DEFAULT --rsource -j $CHAIN_NAME_SMTP

#It’s good practice to have this line in here in case you ever want to modify the chain’s default policy to REJECT
iptables -A INPUT  -p tcp -m tcp --dport $PORT_SSH  -j ACCEPT
iptables -A INPUT  -p tcp -m tcp --dport $PORT_SMTP -j ACCEPT

#tell iptables what to do with packets that get sent here
iptables -A $CHAIN_NAME_SSH -j LOG --log-prefix "iptables deny: " --log-level 7
iptables -A $CHAIN_NAME_SSH -j DROP

iptables -A $CHAIN_NAME_SMTP -j LOG --log-prefix "iptables deny: " --log-level 7
iptables -A $CHAIN_NAME_SMTP -j DROP

#cat <<'EOF' > /etc/logrotate.d/iptables
#/var/log/iptables.log
#{
#  rotate 7
#  daily
#  missingok
#  notifempty
#  delaycompress
#  compress
#  postrotate
#      /etc/init.d/rsyslog reload > /dev/null
#  endscript
#}
#EOF

#cat <<'EOF' >/etc/rsyslog.d/iptables.conf
#:msg,contains,"iptables deny: " /var/log/iptables.log
#& ~
#EOF

#/etc/init.d/rsyslog restart

#VOIP SECTION

# RTP - the media stream
# (related to the port range in /etc/asterisk/rtp.conf) 
iptables -A INPUT -p udp -m udp --dport 10000:20000 -j ACCEPT
# SCCP on TCP port 2000.
iptables -A INPUT -p tcp -m tcp --dport 2000 -j ACCEPT
# SIP on UDP port 5060.
iptables -I INPUT -p udp -m udp --dport 5060 -m string --string "User-Agent: VaxSIPUserAgent" --algo bm --to 65535 -j DROP 
iptables -I INPUT -p udp -m udp --dport 5060 -m string --string "User-Agent: friendly-scanner" --algo bm --to 65535 -j REJECT --reject-with icmp-port-unreachable 
iptables -I INPUT -p udp -m udp --dport 5060 -m string --string "REGISTER sip:" --algo bm -m recent --set --name VOIP --rsource 
iptables -I INPUT -p udp -m udp --dport 5060 -m string --string "REGISTER sip:" --algo bm -m recent --update --seconds 60 --hitcount 12 --rttl --name VOIP --rsource -j DROP 
iptables -I INPUT -p udp -m udp --dport 5060 -m string --string "INVITE sip:" --algo bm -m recent --set --name VOIPINV --rsource 
iptables -I INPUT -p udp -m udp --dport 5060 -m string --string "INVITE sip:" --algo bm -m recent --update --seconds 60 --hitcount 12 --rttl --name VOIPINV --rsource -j DROP 
iptables -I INPUT -p udp -m hashlimit --hashlimit 6/sec --hashlimit-mode srcip,dstport --hashlimit-name tunnel_limit -m udp --dport 5060 -j ACCEPT 
iptables -A INPUT -p udp -m udp --dport 5060 -j ACCEPT
