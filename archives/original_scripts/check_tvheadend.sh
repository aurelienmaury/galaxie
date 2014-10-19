#! /bin/sh

if pgrep userhdhomerun> /dev/null
then
        exit 0
fi
/etc/init.d/dvbhdhomerun-utils restart
wait 5
/etc/init.d/tvheadend restart
