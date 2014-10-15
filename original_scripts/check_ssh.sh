#! /bin/sh

if netstat -plant | grep :22 | grep -c LISTEN > /dev/null
then
        exit 0
fi
/etc/init.d/ssh restart
