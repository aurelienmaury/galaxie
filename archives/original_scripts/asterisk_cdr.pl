#! /usr/bin/perl

use warnings;
use strict;
use Text::CSV;
use Getopt::Long ();

my $cdrCsvIsGmt = defined $ENV{CDRCSV_ISGMT} ? $ENV{CDRCSV_ISGMT} : 1;
my $csv = Text::CSV->new ( { binary => 1 } ) or die "Cannot use CSV: " .Text::CSV->error_diag ();

#my $CDR_CSV_PATH_FILE = '/home/jornech/opt/Asterisk_cdr/Master.csv';
my $CDR_CSV_PATH_FILE = '/var/log/asterisk/cdr-csv/Master.csv';
my $ASTERISK_BIN_PATH = `which asterisk`;
chomp $ASTERISK_BIN_PATH;
my @ASTERISK_DIALPLAN_OUTPUT = `$ASTERISK_BIN_PATH -rx 'dialplan show'`;
chomp @ASTERISK_DIALPLAN_OUTPUT;

my @CDR_CSV_CONTENT_FILE = undef;
my @CDR_CSV_CONTENT_LINE = undef;
my $COUNT_CALL = 1;

# Use for count the sum of duration of a call context.
my $OUTGOING_CALL_TOTAL_BILLSEC  = 0;
my $INCOMING_CALL_TOTAL_BILLSEC  = 0;
my $ANONYMOUS_CALL_TOTAL_BILLSEC = 0;
my $INTERNAL_CALL_TOTAL_BILLSEC  = 0;

my $OUTGOING_CALL_TOTAL_SYSSEC  = 0;
my $INCOMING_CALL_TOTAL_SYSSEC  = 0;
my $ANONYMOUS_CALL_TOTAL_SYSSEC = 0;
my $INTERNAL_CALL_TOTAL_SYSSEC  = 0;

my $OUTGOING_CALL_TOTAL_OF_CALL  = 0;
my $INCOMING_CALL_TOTAL_OF_CALL  = 0;
my $ANONYMOUS_CALL_TOTAL_OF_CALL = 0;
my $INTERNAL_CALL_TOTAL_OF_CALL  = 0;

my $OUTGOING_CALL_TOTAL_ANSWERED  = 0;
my $INCOMING_CALL_TOTAL_ANSWERED  = 0;
my $ANONYMOUS_CALL_TOTAL_ANSWERED = 0;
my $INTERNAL_CALL_TOTAL_ANSWERED  = 0;

my $OUTGOING_CALL_POURCENT_ANSWERED  = 0;
my $INCOMING_CALL_POURCENT_ANSWERED  = 0;
my $ANONYMOUS_CALL_POURCENT_ANSWERED = 0;
my $INTERNAL_CALL_POURCENT_ANSWERED  = 0;

my $CALL_LABEL = undef;

#Is use for search a pattern inside CDR Source"src"
# Generally it's Registred Phone
#Is OUTGOING Call when : ( ($INFO{dcontext} =~ m/$CONTEXT_INTERNAL_PAT/) && ($INFO{dstchannel} =~ m/$CONTEXT_ISP_PAT/))
#Is INCOMING Call when : ( ( $INFO{dst} eq 's') || ( $INFO{dst} eq '~~s~~') && ($INFO{lastapp} eq 'Dial') && ($INFO{dcontext} =~ m/$CONTEXT_OUTGOING_PAT/) )
#Is INTERNAL Call when : ( ($INFO{dcontext} =~ m/$CONTEXT_INTERNAL_PAT/) && ($INFO{dstchannel} !~ m/$CONTEXT_ISP_PAT/))
#Is INCOMING Call when : 
my $CONTEXT_INTERNAL_PAT  = 'appel-interne';
my $CONTEXT_OUTGOING_PAT  = 'appel-entrant';
my $CONTEXT_ANONYMOUS_PAT = 'appel-anonymous';
my $CONTEXT_ISP_PAT       = 'forfait-ovh' ;

my $DEBUG             = 0;
my $DISPLAY_INCOMING  = 0;
my $DISPLAY_OUTGOING  = 0;
my $DISPLAY_ANONYMOUS = 0;
my $DISPLAY_INTERNAL  = 0;
my $DISPLAY_VERSION   = 0;

#VARIABLE DECLARATION
my $VERSION = "0.9";
my %INFO = ();
my $LINE_CSV = undef;
my @LINE_CONTENT = undef;
my $FILE = undef;
my %INDEX_GENERAL = ();
my %INDEX_DIALPLAN = ();

# Get Argvs from command line
Getopt::Long::GetOptions(
   '--incoming'  => sub {$DISPLAY_INCOMING  = 1},
   '--outgoing'  => sub {$DISPLAY_OUTGOING  = 1},
   '--anonymous' => sub {$DISPLAY_ANONYMOUS = 1},
   '--internal'  => sub {$DISPLAY_INTERNAL  = 1},
   '--version'   => sub {$DISPLAY_VERSION   = 1},
   '--debug'     => sub {$DEBUG             = 1},
   '--file=s'    => \$CDR_CSV_PATH_FILE,
)
or usage("Invalid commmand line options.");


if ($DISPLAY_VERSION) {
    print<<EOF;
asterisk_cdr version $VERSION");
Copyright © 2013 Jerome Ornech alias Tuux.
License GPLv3+ : GNU GPL version 3 ou ultérieure
<http://gnu.org/licenses/gpl.html>
Ceci est logiciel libre, vous êtes libre de le modifier et de le redistribuer.
Ce logiciel n'est accompagné d'ABSOLUMENT AUCUNE GARANTIE, dans les limites
autorisees par la loi applicable.
EOF
}

#START
open $FILE, '<:encoding(utf8)', $CDR_CSV_PATH_FILE or die "$CDR_CSV_PATH_FILE: $!";
while ( $LINE_CSV = $csv->getline( $FILE ) ) {
	$INDEX_GENERAL{"$COUNT_CALL"} = [@$LINE_CSV];
	$COUNT_CALL ++;
}
$csv->eof or $csv->error_diag();
close $FILE;
&parse_SetCalledParty;
foreach (sort hashValueAscendingNum (keys(%INDEX_GENERAL))) {
	( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
        $INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};

        print ("\n") 								if $DEBUG;
        print ("------------------------------------\n")			if $DEBUG;
        print ("Call num $_\n")							if $DEBUG;
        print ("------------------------------------\n")			if $DEBUG;
        print ("Asterisk billing account, = $INFO{accountcode}\n")		if $DEBUG;
        print ("Caller*ID number = $INFO{src}\n")				if $DEBUG;
        print ("Destination extension = $INFO{dst}\n")				if $DEBUG;
        print ("Destination context = $INFO{dcontext}\n")			if $DEBUG;
        print ("Caller*ID = $INFO{clid}\n")					if $DEBUG;
        print ("Channel used  = $INFO{channel}\n")				if $DEBUG;
        print ("Destination channel = $INFO{dstchannel}\n")			if $DEBUG;
        print ("Last application = $INFO{lastapp}\n")				if $DEBUG;
        print ("Last application data  = $INFO{lastdata}\n")			if $DEBUG;
        print ("Start of call = ",&time2french_date($INFO{start}),"\n")		if $DEBUG;
        print ("Answer of call = ",&time2french_date($INFO{answer}),"\n")	if $DEBUG;
        print ("End of call = ",&time2french_date($INFO{end}),"\n")		if $DEBUG;
        print ("Total time in system =  $INFO{duration} sec\n")			if $DEBUG;
        print ("Total time call is up = $INFO{billsec} sec\n")			if $DEBUG;
        print ("What happened to the call = $INFO{disposition}\n")		if $DEBUG;
        print ("What flags to use = $INFO{amaflags}\n")				if $DEBUG;
        print ("Unique Channel Identifier = $INFO{uniqueid}\n")			if $DEBUG;
        print ("------------------------------------\n")			if $DEBUG;
}
$CALL_LABEL = 'appel';
#OUTGOING CALLS
if ($DISPLAY_OUTGOING) {
        foreach (keys(%INDEX_GENERAL)) {
                ( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
                $INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
                if ( ($INFO{dcontext} =~ m/$CONTEXT_INTERNAL_PAT/) && ($INFO{dstchannel} =~ m/$CONTEXT_ISP_PAT/)) {
                        $OUTGOING_CALL_TOTAL_OF_CALL = ($OUTGOING_CALL_TOTAL_OF_CALL + 1);
                        $OUTGOING_CALL_TOTAL_BILLSEC = ($OUTGOING_CALL_TOTAL_BILLSEC + $INFO{billsec});
                        $OUTGOING_CALL_TOTAL_SYSSEC = ($OUTGOING_CALL_TOTAL_SYSSEC + $INFO{duration});
			if ( $INFO{disposition} eq 'ANSWERED') {$OUTGOING_CALL_TOTAL_ANSWERED ++;}
				
		}
        }
        if ($OUTGOING_CALL_TOTAL_OF_CALL > 1) { $CALL_LABEL .= 's'}
	print ("\nAppels Sortants: ",$OUTGOING_CALL_TOTAL_OF_CALL," ",$CALL_LABEL,", Total: ",&time2human($OUTGOING_CALL_TOTAL_BILLSEC),"\n");
	&print_legendary;
	foreach (sort hashValueAscendingNum (keys(%INDEX_GENERAL))) {
	        ( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
	        $INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
	        if ( ($INFO{dcontext} =~ m/$CONTEXT_INTERNAL_PAT/) && ($INFO{dstchannel} =~ m/$CONTEXT_ISP_PAT/)) {
			if ($INFO{dst} == "123") {
				$INFO{dst} = "Messagerie OVH";
			}
                	printf "%-20s %-30s %-30s %-8s  %-8s  %-20s\n",
                        	&time2french_date($INFO{start}),
                        	$INFO{clid},
                        	$INFO{dst},
                        	&timeconvertion($INFO{duration}),
                        	&timeconvertion($INFO{billsec}),
				$INFO{disposition}
                        	;
	        }
	}
	if ( $OUTGOING_CALL_TOTAL_ANSWERED > 0 ) {$OUTGOING_CALL_POURCENT_ANSWERED = ((100 * $OUTGOING_CALL_TOTAL_ANSWERED)/$OUTGOING_CALL_TOTAL_OF_CALL);}
	printf "                                                                                   %-8s  %-8s  %s\n",'--------','--------','--------------------';
	printf "                                                                           Total:  %-8s  %-8s  %d%% ANSWERED\n",
		&timeconvertion ($OUTGOING_CALL_TOTAL_SYSSEC),
		&timeconvertion($OUTGOING_CALL_TOTAL_BILLSEC),
		$OUTGOING_CALL_POURCENT_ANSWERED;
}
$CALL_LABEL = 'appel';
#INCOMING CALLS
if ($DISPLAY_INCOMING) {
	foreach (keys(%INDEX_GENERAL)) {
	        ( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
	        $INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
	        if ( $INFO{dcontext} =~ m/$CONTEXT_OUTGOING_PAT/) {
			$INCOMING_CALL_TOTAL_OF_CALL = ($INCOMING_CALL_TOTAL_OF_CALL + 1); 
	       		$INCOMING_CALL_TOTAL_BILLSEC = ($INCOMING_CALL_TOTAL_BILLSEC + $INFO{billsec});
                        $INCOMING_CALL_TOTAL_SYSSEC  = ($INCOMING_CALL_TOTAL_SYSSEC  + $INFO{duration});
			if ( $INFO{disposition} eq 'ANSWERED') {$INCOMING_CALL_TOTAL_ANSWERED ++;}
	        }
	}
        if ($INCOMING_CALL_TOTAL_OF_CALL > 1) { $CALL_LABEL .= 's'}
	print ("\nAppels Entrant: ",$INCOMING_CALL_TOTAL_OF_CALL, " ",$CALL_LABEL,", Total: ",&time2human($INCOMING_CALL_TOTAL_BILLSEC),"\n");
	&print_legendary;
	foreach (sort hashValueAscendingNum (keys(%INDEX_GENERAL))) {
	        ( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
	        $INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
	        if ( ( $INFO{dst} eq 's') || ( $INFO{dst} eq '~~s~~') && ($INFO{lastapp} eq 'Dial') && ($INFO{dcontext} =~ m/$CONTEXT_OUTGOING_PAT/) ) {
			$INFO{dst} = $INFO{lastdata};
		}
	        if ( $INFO{dcontext} =~ m/$CONTEXT_OUTGOING_PAT/) {
                	printf "%-20s %-30s %-30s %-8s  %-8s  %-20s\n",
                        	&time2french_date($INFO{start}),
                        	$INFO{clid},
                        	$INFO{dst},
                        	&timeconvertion($INFO{duration}),
                        	&timeconvertion($INFO{billsec}),
				$INFO{disposition}
                        	;
	        }
	}
	if ( $INCOMING_CALL_TOTAL_ANSWERED > 0 ) {$INCOMING_CALL_POURCENT_ANSWERED = ((100 * $INCOMING_CALL_TOTAL_ANSWERED)/$INCOMING_CALL_TOTAL_OF_CALL);}
	printf "                                                                                   %-8s  %-8s  %s\n",'--------','--------','--------------------';
	printf "                                                                           Total:  %-8s  %-8s  %d%% ANSWERED\n",
		&timeconvertion ($INCOMING_CALL_TOTAL_SYSSEC),&timeconvertion ($INCOMING_CALL_TOTAL_BILLSEC),$INCOMING_CALL_POURCENT_ANSWERED;
	print ("\n");
}
$CALL_LABEL = 'appel';
#ANONYMOUS CALLS
if ($DISPLAY_ANONYMOUS) {
	foreach (keys(%INDEX_GENERAL)) {
  		( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
		$INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
		if ( $INFO{dcontext} =~ m/$CONTEXT_ANONYMOUS_PAT/ ) {
			$ANONYMOUS_CALL_TOTAL_OF_CALL = ($ANONYMOUS_CALL_TOTAL_OF_CALL + 1); 
			$ANONYMOUS_CALL_TOTAL_BILLSEC = ($ANONYMOUS_CALL_TOTAL_BILLSEC + $INFO{billsec});
                        $ANONYMOUS_CALL_TOTAL_SYSSEC  = ($ANONYMOUS_CALL_TOTAL_SYSSEC  + $INFO{duration});
			if ( $INFO{disposition} eq 'ANSWERED') {$ANONYMOUS_CALL_TOTAL_ANSWERED ++;}
	        }
	}
        if ($ANONYMOUS_CALL_TOTAL_OF_CALL > 1) { $CALL_LABEL .= 's'}
	print ("\nAppels Anonyme: ",$ANONYMOUS_CALL_TOTAL_OF_CALL," ",$CALL_LABEL,", Total: ",&time2human($ANONYMOUS_CALL_TOTAL_BILLSEC),"\n");
	&print_legendary;
	foreach (sort hashValueAscendingNum (keys(%INDEX_GENERAL))) {
  	( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
	$INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
	if ( ( $INFO{dst} eq 's') || ( $INFO{dst} eq '~~s~~') && ($INFO{lastapp} eq 'Dial') && ($INFO{dcontext} =~ m/$CONTEXT_OUTGOING_PAT/) ) {
		$INFO{dst} = $INFO{lastdata};
	}
	if ( $INFO{dcontext} =~ m/$CONTEXT_ANONYMOUS_PAT/ ) {
                	printf "%-20s %-30s %-30s %-8s  %-8s  %-20s\n",
                        	&time2french_date($INFO{start}),
                        	$INFO{clid},
                        	$INFO{dst},
                        	&timeconvertion($INFO{duration}),
                        	&timeconvertion($INFO{billsec}),
				$INFO{disposition}
                        	;
	        }
	}
	if ( $ANONYMOUS_CALL_TOTAL_ANSWERED > 0 ) {$ANONYMOUS_CALL_POURCENT_ANSWERED = ((100 * $ANONYMOUS_CALL_TOTAL_ANSWERED)/$ANONYMOUS_CALL_TOTAL_OF_CALL);}
	printf "                                                                                   %-8s  %-8s  %s\n",'--------','--------','--------------------';
	printf "                                                                           Total:  %-8s  %-8s  %d%% ANSWERED\n",
		&timeconvertion ($ANONYMOUS_CALL_TOTAL_SYSSEC),&timeconvertion ($ANONYMOUS_CALL_TOTAL_BILLSEC),$ANONYMOUS_CALL_POURCENT_ANSWERED;
	print ("\n");
}
$CALL_LABEL = 'appel';
#INTERNAL CALLS
if ($DISPLAY_INTERNAL) {
	foreach (keys(%INDEX_GENERAL)) {
        	( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
        	$INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
        	if ( ($INFO{dcontext} =~ m/$CONTEXT_INTERNAL_PAT/) && ($INFO{dstchannel} !~ m/$CONTEXT_ISP_PAT/)) {
			$INTERNAL_CALL_TOTAL_OF_CALL = ($INTERNAL_CALL_TOTAL_OF_CALL + 1);
                	$INTERNAL_CALL_TOTAL_BILLSEC = ($INTERNAL_CALL_TOTAL_BILLSEC + $INFO{billsec});
                        $INTERNAL_CALL_TOTAL_SYSSEC  = ($INTERNAL_CALL_TOTAL_SYSSEC  + $INFO{duration});
			if ( $INFO{disposition} eq 'ANSWERED') {$INTERNAL_CALL_TOTAL_ANSWERED ++;}
        	}
	}
        if ($INTERNAL_CALL_TOTAL_OF_CALL > 1) { $CALL_LABEL .= 's'}
	print ("\nAppels Interne: ",$INTERNAL_CALL_TOTAL_OF_CALL, " ",$CALL_LABEL,", Total: ",&time2human($INTERNAL_CALL_TOTAL_BILLSEC),"\n");
	&print_legendary;
	foreach (sort hashValueAscendingNum (keys(%INDEX_GENERAL))) {
        	( $INFO{accountcode},$INFO{src},$INFO{dst},$INFO{dcontext},$INFO{clid},$INFO{channel},$INFO{dstchannel},$INFO{lastapp},$INFO{lastdata},$INFO{start},
        	$INFO{answer},$INFO{end},$INFO{duration},$INFO{billsec},$INFO{disposition},$INFO{amaflags},$INFO{uniqueid} ) = @{$INDEX_GENERAL{$_}};
        	if ( ($INFO{dcontext} =~ m/$CONTEXT_INTERNAL_PAT/) && ($INFO{dstchannel} !~ m/$CONTEXT_ISP_PAT/)) {
			if ($INDEX_DIALPLAN{$INFO{dst}}) {
				$INFO{dst} = $INDEX_DIALPLAN{$INFO{dst}};
			}
                	printf "%-20s %-30s %-30s %-8s  %-8s  %-20s\n",
                        	&time2french_date($INFO{start}),
                        	$INFO{clid},
                        	$INFO{dst},
                        	&timeconvertion($INFO{duration}),
                        	&timeconvertion($INFO{billsec}),
				$INFO{disposition}
                        	;
        	}
	}
	if ( $INTERNAL_CALL_TOTAL_ANSWERED > 0 ) {$INTERNAL_CALL_POURCENT_ANSWERED = ((100 * $INTERNAL_CALL_TOTAL_ANSWERED)/$INTERNAL_CALL_TOTAL_OF_CALL);}
	printf "                                                                                   %-8s  %-8s  %s\n",'--------','--------','--------------------';
	printf "                                                                           Total:  %-8s  %-8s  %d%% ANSWERED\n",
		&timeconvertion ($INTERNAL_CALL_TOTAL_SYSSEC),&timeconvertion ($INTERNAL_CALL_TOTAL_BILLSEC),$INTERNAL_CALL_POURCENT_ANSWERED;
}

#SUBROUTINE SECTION
sub parse_SetCalledParty {
	my $REGEXPR1 = '.*?';	        # Non-greedy match on filler
	my $REGEXPR2 = '(\\d+)';	# Integer Number 1
	my $REGEXPR3 = '.*?';	        # Non-greedy match on filler
	my $REGEXPR4 = '(\\(.*\\))';	# Round Braces 1
	my $REGEXPR  = $REGEXPR1.$REGEXPR2.$REGEXPR3.$REGEXPR4;
	my $INT      = undef;
	my $STRING   = undef;
	foreach (@ASTERISK_DIALPLAN_OUTPUT) {
		next if ($_ !~ m/SetCalledParty/ );
		if ($_ =~ m/$REGEXPR/is) {	
			$INT=$1;
    			$STRING=$2;
			$STRING =~ s/^\(//; 
			$STRING =~ s/\)$//; 
    			print "$INT $STRING\n" if $DEBUG;
			$INDEX_DIALPLAN{"$INT"} = $STRING;
		}
	}

}
sub timeconvertion {
	#$TIME int in secondes value
	my ($TIME, undef) = @_;
	my $HOUR = int($TIME/ 3600);
	my $MIN  = int(($TIME % 3600) / 60);
	my $SEC  = int($TIME % 60); 
	my $TIME_CONVERTED = sprintf("%02u:%02u:%02u", $HOUR,$MIN,$SEC);
	return ($TIME_CONVERTED);
}

sub time2human {
	#$TIME int in secondes value
	my ($TIME, undef) = @_;
	my $HOUR = int($TIME/ 3600);
	my $MIN  = int(($TIME % 3600) / 60);
	my $SEC  = int($TIME % 60);
	my $TIME_CONVERTED = undef;
	my $HOUR_LABEL = 'Heure';
	my $MIN_LABEL  = 'Minute';
	my $SEC_LABEL  = 'Seconde';
	if ($HOUR > 1) { $HOUR_LABEL = $HOUR_LABEL."s"; }
	if ($MIN  > 1) { $MIN_LABEL  = $MIN_LABEL."s"; }
	if ($SEC  > 1) { $SEC_LABEL = $SEC_LABEL."s"; }
	if ($HOUR > 0) {
		$TIME_CONVERTED = sprintf("%u %s %u %s %u %s", $HOUR,$HOUR_LABEL,$MIN,$MIN_LABEL,$SEC,$SEC_LABEL);
	} else {
		if ($MIN > 0) {
			$TIME_CONVERTED = sprintf("%u %s %u %s", $MIN,$MIN_LABEL,$SEC,$SEC_LABEL);
		} else {
			$TIME_CONVERTED = sprintf("%u %s", $SEC,$SEC_LABEL);
		}
	}  
	return ($TIME_CONVERTED);
}

#It subroutine convert Asterisk Date "YYYY-MM-DD HH:MM:SS" to "DD-MM-YYYY HH:MM:SS"
sub time2french_date {
	my ($STRING_TO_CONVERT, undef) = @_;
	my ($YEAR, $MONTH, $DAY, $HOUR, $MIN, $SEC) = ($STRING_TO_CONVERT =~ m/(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/);
	my $STRING_CONVERTED = "$DAY-$MONTH-$YEAR $HOUR:$MIN:$SEC";   
	return ($STRING_CONVERTED);
}

sub hashValueAscendingNum {
   $INDEX_GENERAL{$a} <=> $INDEX_GENERAL{$b};
}

sub print_legendary {
                	printf "%-20s %-30s %-30s %-8s  %-8s   %-20s\n",
                        	'Date de l\'appel',
                        	'Identification de l\'appelant',
                        	'Destination',
				'Sys',
				'Durée',
                        	'Disposition'
                        	;
                	printf "%-20s %-30s %-30s %-8s  %-8s  %-20s\n",
                        	'-------------------',
                        	'------------------------------',
                        	'------------------------------',
                        	'--------',
				'--------',
                        	'--------------------'
                        	;

}

sub usage {
   my $message = $_[0];
   if (defined $message && length $message) {
      $message .= "\n"
         unless $message =~ /\n$/;
   }

   my $command = $0;
   $command =~ s#^.*/##;

   print STDERR (
      $message,
      "usage: $command --debug --incoming --outgoing --anonymous --lang=fr \n" .
      "       --anonymous Print report of Anonymous Calls\n" .
      "       --incoming  Print report of Incoming Calls\n" .
      "       --internal  Print report of Internal Calls\n" .
      "       --outgoing  Print report of Outgoing Calls\n" .
      "       --debug     Print debug Information\n" .
      "       --help      Print it usage message\n" .
      "       --version   Print the Version of it program\n"
   );

   die("")
}
