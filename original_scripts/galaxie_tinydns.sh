#!/bin/bash
#Variable declaration
SUPERVISE_DIR=/var/lib/supervise
SERVICE_DIR=/etc/service
MULTILOG_DIR=/var/multilog
TINYDNS_UNAME=tinydns
DNSLOG_UNAME=dnslog
DATE=`date +%Y%m%d%H%M%S`
#SERVICE_IP=`ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
SERVICE_IP=`hostname -I`
SERVICE_NAME=tinydns

#Check and Creat Users tinydns ,dnslog
for USER in {"$TINYDNS_UNAME","$DNSLOG_UNAME"}; do
    getent passwd $USER > /dev/null 2&>1
    if [ $? -ne 0 ]; then
        useradd -M -r -d /no/existant -s /no/existant $USER
    fi
done
#Check and Creat necessary directory
for DIR in {"$SUPERVISE_DIR","$SERVICE_DIR","$MULTILOG_DIR"}; do 
    if [[ ! -e $DIR ]]; then
        mkdir -p $DIR
    fi
done
#Configure tinydns 
if [[ `update-service --list | grep -c $SERVICE_NAME` -eq 1 ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_NAME
fi

if [[ -e $SUPERVISE_DIR/$SERVICE_NAME ]]; then
    echo "mv $SUPERVISE_DIR/$SERVICE_NAME $SUPERVISE_DIR/$SERVICE_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_NAME $SUPERVISE_DIR/$SERVICE_NAME.$DATE
fi
echo "tinydns-conf $TINYDNS_UNAME $DNSLOG_UNAME $SUPERVISE_DIR/$SERVICE_NAME $SERVICE_IP"
tinydns-conf $TINYDNS_UNAME $DNSLOG_UNAME $SUPERVISE_DIR/$SERVICE_NAME $SERVICE_IP
#tinydns log management
#Creat $MULTILOG_DIR/$SERVICE_NAME outside /etc normaly /var/multilog
if [[ ! -e $MULTILOG_DIR/$SERVICE_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_NAME
    chown $DNSLOG_UNAME:$DNSLOG_UNAME $MULTILOG_DIR/$SERVICE_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_NAME $MULTILOG_DIR/$SERVICE_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_NAME $MULTILOG_DIR/$SERVICE_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_NAME
    chown $DNSLOG_UNAME:$DNSLOG_UNAME $MULTILOG_DIR/$SERVICE_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_NAME
fi
#Modify $SUPERVISE_DIR/$SERVICE_NAME/log/run script for use $MULTILOG_DIR/$SERVICE_NAME directory
if [[ -e $SUPERVISE_DIR/$SERVICE_NAME/log/run ]]; then
    mv $SUPERVISE_DIR/$SERVICE_NAME/log/run $SUPERVISE_DIR/$SERVICE_NAME/log/run.old
    sed "s|./main|$MULTILOG_DIR/$SERVICE_NAME|g" $SUPERVISE_DIR/$SERVICE_NAME/log/run.old > $SUPERVISE_DIR/$SERVICE_NAME/log/run
    rm $SUPERVISE_DIR/$SERVICE_NAME/log/run.old
    chmod 755 $SUPERVISE_DIR/$SERVICE_NAME/log/run
    if [[ -e $SUPERVISE_DIR/$SERVICE_NAME/log/main ]]; then
        rm -rf $SUPERVISE_DIR/$SERVICE_NAME/log/main
    fi
fi
#tinydns service management
if [[ `update-service --list | grep -c $SERVICE_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR/$SERVICE_NAME
else
    update-service --remove $SUPERVISE_DIR/$SERVICE_NAME
    update-service --add $SUPERVISE_DIR/$SERVICE_NAME
fi
