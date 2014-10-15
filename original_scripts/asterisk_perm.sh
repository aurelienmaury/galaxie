/etc/init.d/asterisk stop
adduser --system --group --home /var/lib/asterisk --no-create-home --gecos "Asterisk PBX" asterisk
adduser asterisk dialout
adduser asterisk audio
chown --recursive asterisk:asterisk /var/lib/asterisk
chown --recursive asterisk:asterisk /var/log/asterisk
chown --recursive asterisk:asterisk /var/run/asterisk
chown --recursive asterisk:asterisk /var/spool/asterisk
chown --recursive asterisk:asterisk /usr/lib/asterisk
chown --recursive asterisk:asterisk /dev/zap
chown --recursive asterisk:asterisk /dev/dahdi
chmod --recursive u=rwX,g=rX,o= /var/lib/asterisk
chmod --recursive u=rwX,g=rX,o= /var/log/asterisk
chmod --recursive u=rwX,g=rX,o= /var/run/asterisk
chmod --recursive u=rwX,g=rX,o= /var/spool/asterisk
chmod --recursive u=rwX,g=rX,o= /usr/lib/asterisk
chmod --recursive u=rwX,g=rX,o= /dev/zap
chmod --recursive u=rwX,g=rX,o= /dev/dahdi
chown --recursive root:asterisk /etc/asterisk
chmod --recursive u=rwX,g=rX,o= /etc/asterisk
chmod g+w /etc/asterisk/voicemail.conf
chmod g+w,+t /etc/asterisk
/etc/init.d/asterisk start
