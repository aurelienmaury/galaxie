#! /usr/bin/perl -w
use strict;
use POSIX ();

#VARIABLE
my $DEBUG = 1;

test_if_user_exist("tuxa");
sub test_if_user_exist {
	my ($username, undef) = @_;
	if( POSIX::access( "/etc/password", &POSIX::R_OK ) ){
		print "have read permission to read password file\n" if $DEBUG;
        	$fd = POSIX::open( "foo" );
                while (<PASSWD>) {
                chomp;
                	if (/^$username:/) { # $username exists
                        	warn "$username already exists in /etc/passwd";
        		}
        	}
		close PASSWD;

    }
}
