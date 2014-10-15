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
