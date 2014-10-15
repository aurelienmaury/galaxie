#! /bin/bash

HOST=the_machine_you_want
DSTDIR=/home/bkp

tar -cvzpf $DSTDIR/$HOST-`date '+%Y%m%d'`.tar.gz \
--exclude=/proc \
--exclude=/sys \
--exclude=/dev/pts \
--exclude=/dev/log \
--exclude=/var/run/courier/authdaemon/socket \
--exclude=/srv/publicfile/0/dlog \
--exclude=/lost+found \
--exclude=/home \
/ && chmod 640 $DSTDIR/$HOST-`date '+%Y%m%d'`.tar.gz

# Remove 7 Days ago backup file
rm $DSTDIR/$HOST-`date --date='7 days ago' +%Y%m%d`.tar.gz

# In Case of remote Archive thing
#rsync -ae ssh $DSTDIRp/$HOST-`date '+%Y%m%d'`.tar.gz USER@HOST:/where/you/want/ && \
#ssh USER@HOST "rm /wher/you/want/$HOST-`date --date='7 days ago' +%Y%m%d`.tar.gz" || \
#echo "Error during remote tranfer
