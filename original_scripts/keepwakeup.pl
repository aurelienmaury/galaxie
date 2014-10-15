#! /usr/bin/perl -w

use strict;
use Net::Ping;
use POSIX qw(strftime);


my $host = 'soleil.galaxie.ici';
my $p = Net::Ping->new();
$p->hires();
my ($ret, $duration, $ip, $date) ;
my $wakeup_bin= `which wakeonlan`;
chomp $wakeup_bin;
my $mac_address = '00:15:c5:57:f9:6c';
my @result;
my $status = 0;
my $control = 0;

print "\n";
while (1) {
	($ret, $duration, $ip) = $p->ping($host, 5.5);
	if ($ret){
			#$date = strftime "%m/%d/%Y-%H:%m:%S", localtime;
                	#print $date." :";
			#printf("$host [ip: $ip] is alive (packet return time: %.2f ms)\n", 1000 * $duration);
			#$control = 1;
		sleep 3;
	} else {
			$date = strftime "%m/%d/%Y-%H:%m:%S", localtime;
			print $date." :";
			@result = `$wakeup_bin $mac_address`;
			print @result;
			sleep 59;
	}
	sleep 1;
	$ret = undef;
}
$p->close();

