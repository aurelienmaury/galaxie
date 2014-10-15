#! /bin/sh

if netstat -plant | grep :80 | grep -c LISTEN > /dev/null
then
        exit 0
fi
/etc/init.d/apache2 restart
