#!/bin/bash
#Variable declaration
SRC_DIR=/usr/src
BUILD_DIR=$SRC_DIR/publicfile
#SUPERVISE_DIR=/srv/publicfile
SUPERVISE_DIR=/var/lib/supervise/publicfile
SUPERVISE_DIR_BASE=/var/lib/supervise
SHARED_DIR=/srv
SERVICE_DIR=/etc/service
MULTILOG_DIR=/var/multilog
PUBLICFILE_UNAME=publicfile
PUBLICFILELOG_UNAME=publicfilelog
DATE=`date +%Y%m%d%H%M%S`
#SERVICE_IP=`ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
#SERVICE_IP=127.0.0.1
SERVICE_IP=`hostname -I`
LOOPBACK_IP=`hostname -i`
HOSTNAME=`hostname`
SERVICE_HTTP_NAME=httpd
SERVICE_FTP_NAME=ftpd
DOMAIN_NAME=galaxie.eu.org
LOCAL_DOMAIN=galaxie.ici
#Check and Creat /var/src/publicfile directory
if [[ -e $BUILD_DIR ]]; then
    rm -rf $BUILD_DIR
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
else
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
fi
#Install the necessary
apt-get install wget tar gzip
wget http://cr.yp.to/publicfile/publicfile-0.52.tar.gz
gunzip publicfile-0.52.tar
tar -xf publicfile-0.52.tar

#Build and install publicfile
if [[ -e $BUILD_DIR/publicfile-0.52 ]]; then
    cd $BUILD_DIR/publicfile-0.52
    echo 'gcc -O2 -include /usr/include/errno.h' > conf-cc
    make
    make setup check
fi
#Check and Creat Users httpd, ftpd, ftpdlog, httpdlog
for USER in {"$PUBLICFILE_UNAME","$PUBLICFILELOG_UNAME"}; do
    getent passwd $USER > /dev/null 2&>1
    if [ $? -ne 0 ]; then
        useradd -M -r -d $SUPERVISE_DIR -s /bin/true $USER
    fi
done
#Check and Creat necessary directory
for DIR in {"$SERVICE_DIR","$MULTILOG_DIR"}; do 
    if [[ ! -e $DIR ]]; then
        mkdir -p $DIR
    fi
done

#Configure publicfile
if [[ `update-service --list | grep -c $SERVICE_HTTP_NAME` -eq 1 ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_HTTP_NAME
fi
if [[ `update-service --list | grep -c $SERVICE_FTP_NAME` -eq 1 ]]; then
    update-service --remove $SUPERVISE_DIR/$SERVICE_FTP_NAME
fi

if [[ -e $SUPERVISE_DIR/$SERVICE_HTTP_NAME ]]; then
    echo "mv $SUPERVISE_DIR/$SERVICE_HTTP_NAME $SUPERVISE_DIR/$SERVICE_HTTP_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_HTTP_NAME $SUPERVISE_DIR/$SERVICE_HTTP_NAME.$DATE
fi

if [[ -e $SUPERVISE_DIR/$SERVICE_FTP_NAME ]]; then
    echo "mv $SUPERVISE_DIR/$SERVICE_FTP_NAME $SUPERVISE_DIR/$SERVICE_FTP_NAME.$DATE"
    mv $SUPERVISE_DIR/$SERVICE_FTP_NAME $SUPERVISE_DIR/$SERVICE_FTP_NAME.$DATE
fi

/usr/local/publicfile/bin/configure $PUBLICFILE_UNAME $PUBLICFILELOG_UNAME $SUPERVISE_DIR $HOSTNAME.$DOMAIN_NAME $HOSTNAME.$LOCAL_DOMAIN $LOOPBACK_IP $SERVICE_IP
#Publicfile log management
#Creat $MULTILOG_DIR/$SERVICE_NAME outside /etc normaly /var/multilog
if [[ ! -e $MULTILOG_DIR/$SERVICE_HTTP_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_HTTP_NAME
    chown $PUBLICFILELOG_UNAME:$PUBLICFILELOG_UNAME $MULTILOG_DIR/$SERVICE_HTTP_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_HTTP_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_HTTP_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_HTTP_NAME $MULTILOG_DIR/$SERVICE_HTTP_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_HTTP_NAME $MULTILOG_DIR/$SERVICE_HTTP_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_HTTP_NAME
    chown $PUBLICFILELOG_UNAME:$PUBLICFILELOG_UNAME $MULTILOG_DIR/$SERVICE_HTTP_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_HTTP_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_HTTP_NAME
fi

if [[ ! -e $MULTILOG_DIR/$SERVICE_FTP_NAME ]]; then
    mkdir -p $MULTILOG_DIR/$SERVICE_FTP_NAME
    chown $PUBLICFILELOG_UNAME:$PUBLICFILELOG_UNAME $MULTILOG_DIR/$SERVICE_FTP_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_FTP_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_FTP_NAME
else
    echo "mv $MULTILOG_DIR/$SERVICE_FTP_NAME $MULTILOG_DIR/$SERVICE_FTP_NAME.$DATE"
    mv $MULTILOG_DIR/$SERVICE_FTP_NAME $MULTILOG_DIR/$SERVICE_FTP_NAME.$DATE
    mkdir -p $MULTILOG_DIR/$SERVICE_FTP_NAME
    chown $PUBLICFILELOG_UNAME:$PUBLICFILELOG_UNAME $MULTILOG_DIR/$SERVICE_FTP_NAME
    chmod 755 $MULTILOG_DIR/$SERVICE_FTP_NAME
    chmod g+s $MULTILOG_DIR/$SERVICE_FTP_NAME
fi

#Modify $SUPERVISE_DIR/$SERVICE_NAME/log/run script for use $MULTILOG_DIR/$SERVICE_NAME directory
if [[ -e $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run ]]; then
    mv $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run.old
    sed "s|./main|$MULTILOG_DIR/$SERVICE_HTTP_NAME|g" $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run.old > $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run
    rm $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run.old
    chmod 755 $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/run
    if [[ -e $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/main ]]; then
        rm -rf $SUPERVISE_DIR/$SERVICE_HTTP_NAME/log/main
    fi
fi

if [[ -e $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run ]]; then
    mv $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run.old
    sed "s|./main|$MULTILOG_DIR/$SERVICE_FTP_NAME|g" $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run.old > $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run
    rm $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run.old
    chmod 755 $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/run
    if [[ -e $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/main ]]; then
        rm -rf $SUPERVISE_DIR/$SERVICE_FTP_NAME/log/main
    fi
fi

#Split httpd and ftpd, change supervise directory, use /var/src for store shared file.
#Change Supervice directory for have httpd and ftp to the same level as other service
mv $SUPERVISE_DIR/$SERVICE_HTTP_NAME $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME
mv $SUPERVISE_DIR/$SERVICE_FTP_NAME $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME
#Creat a Sahred directory for httpd and a other one for ftpd
cp -r $SUPERVISE_DIR/file $SHARED_DIR/$SERVICE_HTTP_NAME
cp -r $SUPERVISE_DIR/file $SHARED_DIR/$SERVICE_FTP_NAME
rm -r $SUPERVISE_DIR/file
#Edit ./run for use new shared directory
if [[ -e $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run ]]; then
    mv $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run.old
    sed "s|$SUPERVISE_DIR/file|$SHARED_DIR/$SERVICE_FTP_NAME|g" $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run.old > $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run
    rm $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run.old
    chmod 755 $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME/run
fi
if [[ -e $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run ]]; then
    mv $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run.old
    sed "s|$SUPERVISE_DIR/file|$SHARED_DIR/$SERVICE_HTTP_NAME|g" $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run.old > $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run
    rm $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run.old
    chmod 755 $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME/run
fi
if [[ -e $SUPERVISE_DIR_BASE/publicfile ]]; then
    rm -rf $SUPERVISE_DIR_BASE/publicfile
fi

cd $SHARED_DIR/$SERVICE_HTTP_NAME
ln -s ./0 www.$DOMAIN_NAME
ln -s ./0 www.$LOCAL_DOMAIN

cd $SHARED_DIR/$SERVICE_FTP_NAME
ln -s ./0 ftp.$DOMAIN_NAME                    
ln -s ./0 ftp.$LOCAL_DOMAIN 

#httpd ftpd service management
if [[ `update-service --list | grep -c $SERVICE_HTTP_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME
else
    update-service --remove $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME
    update-service --add $SUPERVISE_DIR_BASE/$SERVICE_HTTP_NAME
fi

if [[ `update-service --list | grep -c $SERVICE_FTP_NAME` -eq 0 ]]; then
    update-service --add $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME
else
    update-service --remove $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME
    update-service --add $SUPERVISE_DIR_BASE/$SERVICE_FTP_NAME
fi
