#! /bin/bash

#Variable declaration
SRC_DIR=/usr/src
BUILD_DIR=$SRC_DIR/dlog
STAT_FILES=/var/www/galaxie.ici/dlog
HOSTNAME=uranus.galaxie.eu.ici
DLOG_SCRIPT=/root/bin/dlog.sh
CRON_FILE=/etc/cron.d/dlog
#Check and Creat BUILD_DIR directory
if [[ -e $BUILD_DIR ]]; then
    rm -rf $BUILD_DIR
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
else
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
fi
#Install the necessary
apt-get update && \
apt-get install byacc rrdtool flex
#Download from http://dlog.gal.dk/
wget http://dlog.gal.dk/dlog-1.0.0.tar.gz
tar -xzvf dlog-1.0.0.tar.gz
cd dlog-1.0.0
sed "s|wheel|staff|g" configure.pl > configure.pl.mod && mv configure.pl.mod configure.pl
chmod +x configure.pl
./configure.pl --statprefix=$STAT_FILES
make && make install

cat <<'EOF' > $STAT_FILES/index.html
<HTML>
<HEAD>
<TITLE>HOSTNAME dlog</TITLE>
</HEAD>
<BODY>
<H3>Stats of HOSTNAME - dlog - v1.0.0</H3>
<H3>Daily overview&nbsp;-&nbsp;<A HREF="week.html">Weekly overview</A>&nbsp;-&nbsp;<A HREF="month.html">Monthly overview</A>&nbsp;-&nbsp;<A HREF="year.html">Yearly overview</A></H3>
<BR>
<H4>dnscache</H4>
<A HREF="dnscache.html"><IMG SRC="dnscacheday.png"></A><BR>
<A HREF="dnscacheanswers.html"><IMG SRC="dnscacheanswersday.png"></A><BR>
<HR>
<H4>qmail</H4>
<A HREF="qmail.html"><IMG SRC="qmailday.png"></A><BR>
<A HREF="qmailbytes.html"><IMG SRC="qmailbytesday.png"></A><BR>
<A HREF="qmailconcurrency.html"><IMG SRC="qmailconcurrencyday.png"></A><BR>
<A HREF="qmailqueue.html"><IMG SRC="qmailqueueday.png"></A><BR>
<HR>
<BR>
<P>
<A HREF="http://dlog.gal.dk">homepage for dlog</A>
</BODY>
</HTML>
EOF
sed "s|HOSTNAME|$HOSTNAME|g" $STAT_FILES/index.html > $STAT_FILES/index.html.mod && mv $STAT_FILES/index.html.mod $STAT_FILES/index.html
#('axfrdns','dnscache','qmail','qsmtp','rbldns','tinydns','publicfile','qmailqueue','qpsmtpd');
#/usr/local/dlog/bin/dodlog.pl axfrdns init
/usr/local/dlog/bin/dodlog.pl dnscache init
/usr/local/dlog/bin/dodlog.pl qmail init
/usr/local/dlog/bin/dodlog.pl qsmtp init
#/usr/local/dlog/bin/dodlog.pl rbldns init
#/usr/local/dlog/bin/dodlog.pl tinydns init
#/usr/local/dlog/bin/dodlog.pl publicfile init
/usr/local/dlog/bin/dodlog.pl qmailqueue init
/usr/local/dlog/bin/dodlog.pl qpsmtpd init


cat <<'EOF' > $DLOG_SCRIPT
#! /bin/bash
/usr/local/dlog/bin/dodlog.pl dnscache update /var/multilog/dnscache/
/usr/local/dlog/bin/dodlog.pl dnscache graph
/usr/local/dlog/bin/dodlog.pl qmail update /var/multilog/qmail-send/
/usr/local/dlog/bin/dodlog.pl qmail graph
/usr/local/dlog/bin/dodlog.pl qsmtp update /var/multilog/qmail-smtpd/
/usr/local/dlog/bin/dodlog.pl qsmtp update /var/multilog/qmail-smtpsd/
/usr/local/dlog/bin/dodlog.pl qsmtp graph
/usr/local/dlog/bin/dodlog.pl qmailqueue update /var/qmail/bin/qmail-qstat
/usr/local/dlog/bin/dodlog.pl qmailqueue graph
EOF
chmod +x $DLOG_SCRIPT

cat <<'EOF' > $CRON_FILE
*/5 * * * * root DLOG_SCRIPT > /dev/null
#*/10 * * * * root rm STAT_FILES/tinydnsqueries.*.txt > /dev/null
EOF
sed "s|DLOG_SCRIPT|$DLOG_SCRIPT|g" $CRON_FILE > $CRON_FILE.mod && mv $CRON_FILE.mod $CRON_FILE
sed "s|STAT_FILES|$STAT_FILES|g" $CRON_FILE > $CRON_FILE.mod && mv $CRON_FILE.mod $CRON_FILE
#Clenup and Resize images , i delete http://dlog.gal.dk sorry guy, everyone tink that dlog.gal.dk stats
sed "s|-v \\\\\"http://dlog.gal.dk\\\\\"|-h 300 -w 700|g" /usr/local/dlog/bin/dodlog.pl > /usr/local/dlog/bin/dodlog.pl.mod && mv /usr/local/dlog/bin/dodlog.pl.mod /usr/local/dlog/bin/dodlog.pl
chmod +x /usr/local/dlog/bin/dodlog.pl

#Creat for the frist time all png files
$DLOG_SCRIPT
