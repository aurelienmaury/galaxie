#! /usr/bin/perl -w

use strict;

my $NETSTAT_BIN = `which netstat`;
my $GREP_BIN = `which grep`;
my $SCCP_PORT = '2000';
chomp ($NETSTAT_BIN,$GREP_BIN);
my $RESULT = `$NETSTAT_BIN -plantu | $GREP_BIN -i listen | $GREP_BIN -c $SCCP_PORT`;
my @RESULT = '';
chomp ($RESULT);

if ($RESULT == 0) {
        `killall asterisk`;
        @RESULT = `/etc/init.d/asterisk restart`;
        print @RESULT;
}

