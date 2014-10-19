#!/bin/sh
#Prepare Date for send the previous mount report
DATE=`date --date='1 months ago' +%Y-%m`
CSV_DIR=/var/log/asterisk/cdr-csv
CSV_FILE=$CSV_DIR/Master.csv

if [ -f $CSV_FILE ]; then
     cat $CSV_FILE | grep $DATE > $CSV_DIR/cdr-$DATE.csv
     chmod 640 $CSV_DIR/cdr-$DATE.csv
    /root/bin/asterisk_cdr.pl --incoming --outgoing --anonymous --file=$CSV_DIR/cdr-$DATE.csv > $CSV_DIR/cdr-$DATE.txt
    cat $CSV_DIR/cdr-$DATE.txt |  iconv -f utf-8 -t latin1 |\
    enscript -d PDF \
    --header='Rapport du %D{%a. %d/%m/%Y} - %C ||Asterisk galaxie.eu.org' \
    -fCourier7 \
     -o $CSV_DIR/cdr-$DATE.pdf
     mutt -s "Asterisk: Rapport téléphonique du $DATE" -a "$CSV_DIR/cdr-$DATE.pdf" -c lezmy -c tuxa < \
    $CSV_DIR/cdr-$DATE.txt
fi
