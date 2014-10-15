#!/bin/sh
# verifie si un trunk est bloqué

LOG=/var/log/sip_reload.txt
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

asterisk -rx "sip show registry" | grep "No Authentication" > /dev/null

if [ $? = 0 ] ; then
date >> $LOG
asterisk -rx "sip show registry" >> $LOG
asterisk -rx "sip reload"
asterisk -rx "sip show registry" >> $LOG

echo "######" >> $LOG
fi
