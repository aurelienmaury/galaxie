#! /bin/sh

if netstat -plant | grep :3306 | grep -c LISTEN > /dev/null
then
        exit 0
fi
/etc/init.d/mysql restart
