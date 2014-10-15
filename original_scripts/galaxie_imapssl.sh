#!/bin/bash
#Variable declaration
SRC_DIR=/usr/src
SUPERVISE_DIR=/var/lib/supervise
SERVICE_DIR=/etc/service
MULTILOG_DIR=/var/multilog
DATE=`date +%Y%m%d%H%M%S`
SERVICE_IP=192.168.1.70
SERVICE_NAME=imapssl
LOG_USER=root
LOG_GROUP=root

apt-get install courier-authdaemon courier-imap-ssl courier-authlib libgamin0
/etc/init.d/courier-imap stop
/etc/init.d/courier-imap-ssl stop
/etc/init.d/courier-authdaemon start

#Creat supervice directory for imapssl
#The qmail-send process is the queue manager for a qmail system
if [[ -e $SUPERVISE_DIR/$SERVICE_NAME ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_NAME
    echo "mv $SUPERVISE_DIR/$SERVICE_NAME $SUPERVISE_DIR/$SERVICE_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_NAME $SUPERVISE_DIR/$SERVICE_NAME.$DATE
fi
mkdir -m 1755 $SUPERVISE_DIR/$SERVICE_NAME
cd $SUPERVISE_DIR/$SERVICE_NAME
wget --quiet --output-document service-imapssl-run https://qmail.jms1.net/scripts/service-imapssl-run
mv service-imapssl-run run
chmod 700 run
mkdir -m 755 log
cd log
wget --quiet --output-document service-any-log-run http://qmail.jms1.net/scripts/service-any-log-run
mv service-any-log-run run
#Set the common configuration for imapssl
#Set the IP
sed "s|SSLADDRESS=unset|SSLADDRESS=$SERVICE_IP|g" run > run.mod && mv run.mod run
sed "s|SSLPORT=unset|SSLPORT=$SERVICE_IP|g" run > run.mod && mv run.mod run
chmod 700 run

#Creat $MULTILOG_DIR/$SERVICE_NAME outside /etc normaly /var/multilog
if [[ ! -e $MULTILOG_DIR/$SERVICE_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_NAME
    chown $LOG_USER:$LOG_GROUP $MULTILOG_DIR/$SERVICE_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_NAME $MULTILOG_DIR/$SERVICE_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_NAME $MULTILOG_DIR/$SERVICE_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_NAME
    chown $LOG_USER:$LOG_GROUP $MULTILOG_DIR/$SERVICE_NAME
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
#$SERVICE_NAME service management
if [[ `update-service --list | grep -c $SERVICE_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR/$SERVICE_NAME
else
    update-service --remove $SUPERVISE_DIR/$SERVICE_NAME
    update-service --add $SUPERVISE_DIR/$SERVICE_NAME
fi
