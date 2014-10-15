#!/bin/bash
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
SERVICE_NAME=qmail
SERVICE_SEND_NAME=qmail-send
SERVICE_SMTP_NAME=qmail-smtpd
QMAIL_DIR=/var/qmail


create_users_and_groups(){
	#Creation of "nofiles" group
	groupadd -r nofiles
	#Creation of "alias" system user
	getent passwd alias > /dev/null 2&>1
	if [ $? -ne 0 ]; then
		useradd -M -r -g nofiles -s /nonexistent -d $QMAIL_DIR/alias alias
	fi
	#Creation of "qmaild" system user
        getent passwd qmaild > /dev/null 2&>1
        if [ $? -ne 0 ]; then
                useradd -M -r -g nofiles -s /nonexistent -d $QMAIL_DIR qmaild
        fi
	#Creation of "qmaill" system user
        getent passwd qmaill > /dev/null 2&>1
        if [ $? -ne 0 ]; then
                useradd -M -r -g nofiles -s /nonexistent -d $QMAIL_DIR qmaill
        fi
	#Creation of "qmailp" system user
        getent passwd qmailp > /dev/null 2&>1
        if [ $? -ne 0 ]; then
                useradd -M -r -g nofiles -s /nonexistent -d $QMAIL_DIR qmailp
        fi
	#Creation of "qmail" group
	groupadd -r qmail
        #Creation of "qmailq" system user
        getent passwd qmailq > /dev/null 2&>1
        if [ $? -ne 0 ]; then
                useradd -M -r -g qmail -s /nonexistent -d $QMAIL_DIR qmailq
        fi
        #Creation of "qmailr" system user
        getent passwd qmailr > /dev/null 2&>1
        if [ $? -ne 0 ]; then
                useradd -M -r -g qmail -s /nonexistent -d $QMAIL_DIR qmailr
        fi
        #Creation of "qmails" system user
        getent passwd qmails > /dev/null 2&>1
        if [ $? -ne 0 ]; then
                useradd -M -r -g qmail -s /nonexistent -d $QMAIL_DIR qmails
        fi
}

create_users_and_groups

#Check and Creat /var/src/qmail directory
if [[ -e $BUILD_DIR ]]; then
	rm -rf $BUILD_DIR
	mkdir -p $BUILD_DIR
	cd $BUILD_DIR
else
	mkdir -p $BUILD_DIR
	cd $BUILD_DIR
fi

apt-get install libssl-dev libssl1.0.0 ca-certificates
wget http://cr.yp.to/software/qmail-1.03.tar.gz
wget http://qmail.jms1.net/patches/qmail-1.03-jms1-7.10.patch
wget http://www.qmail.org/moni.csi.hu/pub/glibc-2.3.1/qmail-1.03.errno.patch
tar xvzf qmail-1.03.tar.gz
mv qmail-1.03 qmail-1.03-jms1-7.10
cd qmail-1.03-jms1-7.10
patch < ../qmail-1.03-jms1-7.10.patch
#patch < ../qmail-1.03.errno.patch
make
make man
make setup check

#Stop and remove Exim
/etc/init.d/exim4 stop
dpkg --ignore-depends=exim4 -r exim4
dpkg --ignore-depends=exim4-daemon-light -r exim4-daemon-light

#If you are using sendmail or postfix :
dpkg --purge --ignore-depends=postfix postfix
dpkg --purge sendmail sendmail-base sendmail-bin sendmail-cf

#Install a pseudo MTA (mta-local_1.0_all.deb) to avoid problem within Debian system
wget http://qmailrocks.thibs.com/downloads/deb-packages/mta-local_1.0_all.deb
dpkg -i ./mta-local_1.0_all.deb

#Create Symlink to use Qmail instead of the default MTA
rm -f /usr/lib/sendmail
rm -f /usr/sbin/sendmail
ln -s $QMAIL_DIR/bin/sendmail /usr/lib/sendmail
ln -s $QMAIL_DIR/bin/sendmail /usr/sbin/sendmail

echo ./Maildir > $QMAIL_DIR/control/defaultdelivery
#Set some configuration (You can find more on http://www.lifewithqmail.com/lwq.html#configuration)
echo 255 > $QMAIL_DIR/control/concurrencyremote
echo 30 > $QMAIL_DIR/control/concurrencyincoming
echo 3 > $QMAIL_DIR/control/spfbehavior
echo postmaster@$DOMAIN > $QMAIL_DIR/control/bouncefrom
echo $DOMAIN > $QMAIL_DIR/control/doublebouncehost
echo postmaster > $QMAIL_DIR/control/doublebounceto

cd $QMAIL_DIR/control/
chmod 644 bouncefrom doublebouncehost doublebounceto concurrencyremote concurrencyincoming spfbehavior

Set maximum message size to be 8Mb
echo '8000000' > $QMAIL_DIR/control/databytes

Set 30 seconds as timeout
echo 30 > $QMAIL_DIR/control/timeoutsmtpd 


#Creat supervice directory for qmail-send
#The qmail-send process is the queue manager for a qmail system
if [[ -e $SUPERVISE_DIR/$SERVICE_SEND_NAME ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_SEND_NAME
    echo "mv $SUPERVISE_DIR/$SERVICE_SEND_NAME $SUPERVISE_DIR/$SERVICE_SEND_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_SEND_NAME $SUPERVISE_DIR/$SERVICE_SEND_NAME.$DATE
fi
mkdir -m 1755 $SUPERVISE_DIR/$SERVICE_SEND_NAME
cd $SUPERVISE_DIR/$SERVICE_SEND_NAME
wget --quiet --output-document service-qmail-send-run https://qmail.jms1.net/scripts/service-qmail-send-run
mv service-qmail-send-run run
chmod 700 run
mkdir -m 755 log
cd log
wget --quiet --output-document service-any-log-run http://qmail.jms1.net/scripts/service-any-log-run
mv service-any-log-run run
chmod 700 run

#Creat $MULTILOG_DIR/$SERVICE_SEND_NAME outside /etc normaly /var/multilog
if [[ ! -e $MULTILOG_DIR/$SERVICE_SEND_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_SEND_NAME
    chown $QMAILL_UNAME:root $MULTILOG_DIR/$SERVICE_SEND_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_SEND_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_SEND_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_SEND_NAME $MULTILOG_DIR/$SERVICE_SEND_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_SEND_NAME $MULTILOG_DIR/$SERVICE_SEND_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_SEND_NAME
    chown $QMAILL_UNAME:root $MULTILOG_DIR/$SERVICE_SEND_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_SEND_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_SEND_NAME
fi
#Modify $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run script for use $MULTILOG_DIR/$SERVICE_SEND_NAME directory
if [[ -e $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run ]]; then
    mv $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run.old
    sed "s|./main|$MULTILOG_DIR/$SERVICE_SEND_NAME|g" $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run.old > $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run
    rm $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run.old
    chmod 755 $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/run
    if [[ -e $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/main ]]; then
        rm -rf $SUPERVISE_DIR/$SERVICE_SEND_NAME/log/main
    fi
fi
#$SERVICE_SEND_NAME service management
if [[ `update-service --list | grep -c $SERVICE_SEND_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR/$SERVICE_SEND_NAME
else
    update-service --remove $SUPERVISE_DIR/$SERVICE_SEND_NAME
    update-service --add $SUPERVISE_DIR/$SERVICE_SEND_NAME
fi

# QMAIL SMTP
#Creat supervice directory for $SERVICE_SMTP_NAME
if [[ -e $SUPERVISE_DIR/$SERVICE_SMTP_NAME ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_SMTP_NAME
    echo "mv $SUPERVISE_DIR/$SERVICE_SMTP_NAME $SUPERVISE_DIR/$SERVICE_SMTP_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_SMTP_NAME $SUPERVISE_DIR/$SERVICE_SMTP_NAME.$DATE
fi
mkdir -m 1755 $SUPERVISE_DIR/$SERVICE_SMTP_NAME
cd $SUPERVISE_DIR/$SERVICE_SMTP_NAME
wget --quiet --output-document service-qmail-smtpd-run http://qmail.jms1.net/scripts/service-qmail-smtpd-run

#Set the common configuration for QMAIL SMTP
#Set the IP
sed "s|IP=unset|IP=$SERVICE_IP|g" service-qmail-smtpd-run > run.mod && mv run.mod run
#Change the smtp.cdb path 
sed "s|/etc/tcp/smtp.cdb|$SUPERVISE_DIR/$SERVICE_SMTP_NAME/tcp.cdb|g" run > run.mod && mv run.mod run
#PORT=25
sed "s|PORT=.*|PORT=25|g" run > run.mod && mv run.mod run
#SSL=0
sed "s|SSL=.*|SSL=O|g" run > run.mod && mv run.mod run
#FORCE_TLS=0
sed "s|FORCE_TLS=.*|FORCE_TLS=0|g" run > run.mod && mv run.mod run
#DENY_TLS=0
sed "s|DENY_TLS=.*|DENY_TLS=0|g" run > run.mod && mv run.mod run
#AUTH=1
sed "s|AUTH=.*|AUTH=0|g" run > run.mod && mv run.mod run
#REQUIRE_AUTH=0
sed "s|REQUIRE_AUTH=.*|REQUIRE_AUTH=0|g" run > run.mod && mv run.mod run
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

#Creat $MULTILOG_DIR/$SERVICE_SMTP_NAME outside /etc normaly /var/multilog
if [[ ! -e $MULTILOG_DIR/$SERVICE_SMTP_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_SMTP_NAME
    chown $QMAILL_UNAME:root $MULTILOG_DIR/$SERVICE_SMTP_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_SMTP_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_SMTP_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_SMTP_NAME $MULTILOG_DIR/$SERVICE_SMTP_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_SMTP_NAME $MULTILOG_DIR/$SERVICE_SMTP_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_SMTP_NAME
    chown $QMAILL_UNAME:root $MULTILOG_DIR/$SERVICE_SMTP_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_SMTP_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_SMTP_NAME
fi
#Modify $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run script for use $MULTILOG_DIR/$SERVICE_SMTP_NAME directory
if [[ -e $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run ]]; then
    mv $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run.old
    sed "s|./main|$MULTILOG_DIR/$SERVICE_SMTP_NAME|g" $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run.old > $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run
    rm $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run.old
    chmod 755 $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/run
    if [[ -e $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/main ]]; then
        rm -rf $SUPERVISE_DIR/$SERVICE_SMTP_NAME/log/main
    fi
fi



#$SERVICE_SMTP_NAME service management
if [[ `update-service --list | grep -c $SERVICE_SMTP_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR/$SERVICE_SMTP_NAME
else
    update-service --remove $SUPERVISE_DIR/$SERVICE_SMTP_NAME
    update-service --add $SUPERVISE_DIR/$SERVICE_SMTP_NAME
fi


