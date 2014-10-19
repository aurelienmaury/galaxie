#! /bin/bash

#Variable declaration
SRC_DIR=/usr/src
BUILD_DIR=$SRC_DIR/qmail
SUPERVISE_DIR=/var/lib/supervise
SERVICE_DIR=/etc/service
MULTILOG_DIR=/var/multilog
QMAILL_UNAME=qmaill
DATE=`date +%Y%m%d%H%M%S`
SERVICE_IP=192.168.1.69
ME=mx1.galaxie.eu.org
DOMAIN=galaxie.eu.org
SERVICE_SMTPS_NAME=qmail-smtpsd
QMAIL_DIR=/var/qmail


cd $SRC_DIR
wget http://www.fehcom.de/ipnet/ucspi-ssl/ucspi-ssl-0.93.tgz
tar -xzf ucspi-ssl-0.93.tgz
cd $SRC_DIR/host/superscript.com/net/ucspi-ssl-0.93
package/compile
package/man
cd $SRC_DIR/host/superscript.com/net/ucspi-ssl-0.93/compile
cp https@ /usr/local/bin/
cp sslcat /usr/local/bin/
cp sslclient /usr/local/bin/
cp sslconnect /usr/local/bin/
cp sslprint /usr/local/bin/
cp sslserver /usr/local/bin/
rm -rf $SRC_DIR/host

# QMAIL SMTPS
#Creat supervice directory for $SERVICE_SMTPS_NAME
if [[ -e $SUPERVISE_DIR/$SERVICE_SMTPS_NAME ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_SMTPS_NAME
    echo "mv $SUPERVISE_DIR/$SERVICE_SMTPS_NAME $SUPERVISE_DIR/$SERVICE_SMTPS_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_SMTPS_NAME $SUPERVISE_DIR/$SERVICE_SMTPS_NAME.$DATE
fi
mkdir -m 1755 $SUPERVISE_DIR/$SERVICE_SMTPS_NAME
cd $SUPERVISE_DIR/$SERVICE_SMTPS_NAME
wget --quiet --output-document service-qmail-smtpd-run http://qmail.jms1.net/scripts/service-qmail-smtpd-run

#Set the common configuration for QMAIL SMTP
#Set the IP
sed "s|IP=unset|IP=$SERVICE_IP|g" service-qmail-smtpd-run > run.mod && mv run.mod run
#Change the smtp.cdb path 
sed "s|/etc/tcp/smtp.cdb|$SUPERVISE_DIR/$SERVICE_SMTPS_NAME/tcp.cdb|g" run > run.mod && mv run.mod run
#PORT=25
sed "s|PORT=.*|PORT=465|g" run > run.mod && mv run.mod run
#SSL=0
sed "s|SSL=.*|SSL=1|g" run > run.mod && mv run.mod run
#FORCE_TLS=0
sed "s|FORCE_TLS=.*|FORCE_TLS=0|g" run > run.mod && mv run.mod run
#DENY_TLS=0
sed "s|DENY_TLS=.*|DENY_TLS=0|g" run > run.mod && mv run.mod run
#AUTH=1
sed "s|AUTH=.*|AUTH=1|g" run > run.mod && mv run.mod run
#REQUIRE_AUTH=0
sed "s|REQUIRE_AUTH=.*|REQUIRE_AUTH=1|g" run > run.mod && mv run.mod run
#ALLOW_INSECURE_AUTH=0
sed "s|ALLOW_INSECURE_AUTH=.*|ALLOW_INSECURE_AUTH=0|g" run > run.mod && mv run.mod run

chmod 700 run
#MAnagement of tcp.cdb
cat <<'EOF' > Makefile
SHELL=/bin/sh

tcp.cdb: tcp
	/usr/bin/tcprules tcp.cdb tcp.tmp < tcp
EOF

cat <<'EOF' > tcp
127.:allow,RELAYCLIENT=""
:allow 
EOF
make


mkdir -m 755 log
cd log
wget --quiet --output-document service-any-log-run http://qmail.jms1.net/scripts/service-any-log-run
mv service-any-log-run run
chmod 700 run

echo "$ME" > $QMAIL_DIR/control/me

#Creat $MULTILOG_DIR/$SERVICE_SMTPS_NAME outside /etc normaly /var/multilog
if [[ ! -e $MULTILOG_DIR/$SERVICE_SMTPS_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_SMTPS_NAME
    chown $QMAILL_UNAME:root $MULTILOG_DIR/$SERVICE_SMTPS_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_SMTPS_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_SMTPS_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_SMTPS_NAME $MULTILOG_DIR/$SERVICE_SMTPS_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_SMTPS_NAME $MULTILOG_DIR/$SERVICE_SMTPS_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_SMTPS_NAME
    chown $QMAILL_UNAME:root $MULTILOG_DIR/$SERVICE_SMTPS_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_SMTPS_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_SMTPS_NAME
fi
#Modify $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run script for use $MULTILOG_DIR/$SERVICE_SMTPS_NAME directory
if [[ -e $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run ]]; then
    mv $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run.old
    sed "s|./main|$MULTILOG_DIR/$SERVICE_SMTPS_NAME|g" $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run.old > $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run
    rm $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run.old
    chmod 755 $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/run
    if [[ -e $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/main ]]; then
        rm -rf $SUPERVISE_DIR/$SERVICE_SMTPS_NAME/log/main
    fi
fi

#$SERVICE_SMTPS_NAME service management
if [[ `update-service --list | grep -c $SERVICE_SMTPS_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR/$SERVICE_SMTPS_NAME
else
    update-service --remove $SUPERVISE_DIR/$SERVICE_SMTPS_NAME
    update-service --add $SUPERVISE_DIR/$SERVICE_SMTPS_NAME
fi

