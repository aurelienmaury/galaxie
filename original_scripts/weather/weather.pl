#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
use JSON;
use LWP::UserAgent::Determined;
use utf8;
binmode STDOUT, 'utf8';
use GD;
use Getopt::Long;
use Pod::Usage;
use Try::Tiny;
do "init_colors.pl";



my $city     = "guitrancourt";
my $iconsdir = "/root/bin/weather/icons";
my $debug    = 1;
my $picture  = undef;
my $daily    = undef;
my $text     = undef;
my $version  = "0.71";
my $man      = undef;
my $help     = undef;


GetOptions (
	"city=s"  => \$city,
	"debug"   => \$debug,
	"text"    => \$text,
	"picture" => \$picture,
	"daily"   => \$daily,
	"version" => \$version,
	"help|?" => \$help, 
	"man"    => \$man
) or pod2usage(2);
pod2usage(1) if $help;
pod2usage(-exitval => 0, -verbose => 2) if $man;

if (($text) || ($picture)) {
	my $weather_json = JSON->new();
	#my $weather_json = JSON->new->allow_nonref;

	my $browser = LWP::UserAgent::Determined->new;
	my $response =$browser->get("http://api.openweathermap.org/data/2.5/weather?q=$city&unit=metric&lang=fr");
	my $weather_response = $response->decoded_content;
	# it prints: a is positive
	#Small clean up of the structure
	$weather_response =~ s/\[//g;
	$weather_response =~ s/\]//g;
	try {
		my $weather_reports = $weather_json->decode( $weather_response );
		print  Dumper($weather_reports) if $debug;
	        city_weather($weather_reports) if $text;
        	#creat_moon_picture($weather_reports);
        	creat_picture($weather_reports) if $picture;
	} catch {
		exit(0);
	}	

}
if ($daily) {
	my $daily_json = JSON->new->allow_nonref;
	my $daily_response = get("http://api.openweathermap.org/data/2.5/forecast/daily?q=$city&mode=json&units=metric&cnt=2");
	die "Couldn't get weather" unless defined $daily_response;
        #$daily_response =~ s/\]//g;
        #$daily_response =~ s/\[//g;
        my $daily_reports = $daily_json->decode( $daily_response );
	print  Dumper($daily_reports->{$city->line => [1,2]});
        print  Dumper($daily_reports) if $debug;


}
sub city_weather {
	my $city = shift;
	$city->{weather}{description} =~ s/^([a-z])/\u$1/;
	$city->{weather}{description} =~ s/\x{c3}\x{a9}/é/g;
	my $wind_description = to_wind_description($city->{wind}{speed});
	my $wind_direction   = to_direction($city->{wind}{deg});
	my $temp = to_celcius($city->{main}{temp});
	format STDOUT =
@<<<<<<<<<<<<<<< @>>>> @<<<
'Température :', $temp, ' C°'  
@<<<<<<<<<<<<<<<<< @>>>> @<<<
'Humidité :', $city->{main}{humidity}, ' %'  
@<<<<<<<<<<<<<<<< @>>>> @<<<
'Préssion :', $city->{main}{pressure}, ' hPa'
@<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
$city->{weather}{description}
@<<<<<<<<<<<<<<<<<<<<<<<<< D: @<<< 
$wind_description, $wind_direction
.
write STDOUT;
}

sub to_direction {
    my $direction = shift;
    return "Nord             N  "
        if (($direction >= "348.75") && ($direction <= "360") || ($direction >= "0") && ($direction <= "11.25"));
    return "nord-nord-est    NNE"
        if ( ($direction >= "11.25")  && ($direction <= "33.75")  );
    return "nord-est         NE "
        if ( ($direction >= "33.75")  && ($direction <= "56.25")  );
    return "est-nord-est     ENE"
        if ( ($direction >= "56.25")  && ($direction <= "78.75")  );
    return "est              E  "
        if ( ($direction >= "78.75")  && ($direction <= "101.25") );
    return  "est-sud-est     ESE"
        if ( ($direction >= "101.25") && ($direction <= "123.75") );
    return "sud-est          SE "
        if ( ($direction >= "123.75") && ($direction <= "146.25") );
    return "sud-sud-est      SSE"
        if ( ($direction >= "146.25") && ($direction <= "168.75") );
    return "Sud              S  "
        if ( ($direction >= "168.75") && ($direction <="191.25") );
    return  "sud-sud-ouest   SSO"
	if ( ($direction >= "191.25") && ($direction <= "213.75") );
    return  "sud-ouest       S0 "
	if ( ($direction >= "213.75") && ($direction <= "236.25") );
    return  "ouest-sud-ouest 0SO"
	if ( ($direction >= "236.25") && ($direction <= "258.75") );
    return  "ouest           O  "
	if ( ($direction >= "258.75") && ($direction <= "281.25") );
    return  "ouest-nord-ouest ONO"
	if ( ($direction >= "281.25") && ($direction <= "303.75") );
    return  "nord-ouest      N0 "
	if ( ($direction >= "303.75") && ($direction <= "326.25") );
    return  "nord-nord-ouest NNO"
	if ( ($direction >= "326.25") && ($direction <= "348.75") );
}


sub to_wind_description {
	my $speed = shift;
	return "Calme"
		if ( ($speed >= "0.000")    && ($speed <= "0.299")  );
	return "Très légère brise"
		if ( ($speed >= "0.300")  && ($speed <= "1.599")  );
	return "Légère brise"
		if ( ($speed >= "1.600")  && ($speed <= "3.399")  );
	return "Petite brise"
		if ( ($speed >= "3.400")  && ($speed <= "5.499")  );
	return "Jolie brise"
		if ( ($speed >= "5.500")  && ($speed <= "7.999")  );
	return "Bonne brise"
		if ( ($speed >= "8.000")  && ($speed <= "10.799") );
	return "Vent frais"
		if ( ($speed >= "10.800") && ($speed <= "13.899") );
	return "Grand frais"
		if ( ($speed >= "13.900") && ($speed <= "17.199") );
	return "Coup de vent"
		if ( ($speed >= "17.200") && ($speed <= "20.799") );
	return "Fort coup de vent"
		if ( ($speed >= "20.800") && ($speed <= "24.499") );
	return "Tempête"
		if ( ($speed >= "24.500") && ($speed <= "28.499") );
	return "Violente tempête"
		if ( ($speed >= "28.500") && ($speed <= "32.699") );
	return "Ouragan"
		if ( ($speed >= "32.700") );
}

sub to_celcius { 
	my $k = shift;
	my $c = undef;
	$c = $k - 274.16 ;
	$c = sprintf("%.2f", $c);
	return($c);
}

sub time_diff {
    my @time1 = split(/:/, shift);
    my @time2 = split(/:/, shift);
    my $time1Minutes = int($time1[0])*60 + $time1[1];
    my $time2Minutes = int($time2[0])*60 + $time2[1];
    
    return $time2Minutes - $time1Minutes;
}

sub creat_moon_picture {
        my $city = shift;
        my $im = new GD::Image(20, 20);
        my $x = 0;
        my $y = 0;
	my $x1 = 10;
	my $y1 = 10;
	my $width = 20;
	my $height = 20;

	my ( $MoonPhase,
	     $MoonIllum,
             $MoonAge,
             $MoonDist,
             $MoonAng,
             $SunDist,
             $SunAng ) = phase();

        # Allocate some colors
        my $white = $im->colorAllocate(255,255,255);
        my $black = $im->colorAllocate(0,0,0);
        my $gray1 = $im->colorAllocate(64,64,64);
        my $gray2 = $im->colorAllocate(128,128,128);

        # Make the background transparent and interlaced
        $im->transparent($white);
        $im->interlaced('true');
	
	#Creat a Dark disk for the background
	$im->arc($x1, $y1, $width, $height, 0, 360, $black);
	# And fill it with red
   	$im->fill($x1,$y1,$black);

	#Creat a White disk for the hide
        $im->arc($x1+5, $y1, $width, $height, 0, 360, $white);
        # And fill it with red
        $im->fill($x1,$y1,$white);

        # Open a file for writing 
        open(PICTURE, ">moon.png") or die("Cannot open file for writing");

        # Make sure we are writing to a binary stream
        binmode PICTURE;

        # Convert the image to PNG and print it to the file PICTURE
        print PICTURE $im->png;
        close PICTURE;


}

sub creat_picture {
        my $city = shift;
#        my $icon = get("http://http://openweathermap.org/img/w/$city->{weather}{icon}.png");
        $city->{weather}{description} =~ s/^([a-z])/\u$1/;
        $city->{weather}{description} =~ s/\x{c3}\x{a9}/é/g;
	$city->{weather}{description} =~ s/\x{c3}\x{a8}/è/g;
        my $wind_description = to_wind_description($city->{wind}{speed});
        my $wind_direction = sprintf("%d", $city->{wind}{deg}); 
	my $wind_direction_text = to_direction($city->{wind}{deg});
	$wind_direction_text =~ s/^([a-z])/\u$1/;
        my $temp = sprintf("%d", to_celcius($city->{main}{temp}));
        #my $sunrise_value = sun_rise($city->{coord}{lon},$city->{coord}{lat});
	#my $sunset_value = sun_set($city->{coord}{lon},$city->{coord}{lat});
	my ($sunrise_sec,$sunrise_min,$sunrise_hour,undef,undef,undef,undef,undef,undef) = localtime($city->{sys}{sunrise});
	my ($sunet_sec,$sunset_min,$sunset_hour,undef,undef,undef,undef,undef,undef) = localtime($city->{sys}{sunset});
	#my $sunrise_value = "$sunrise_hour:$sunrise_min:$sunrise_sec"; 
        #my $sunset_value = "$sunset_hour:$sunset_min:$sunet_sec";
	#Force 2 digit
 	$sunrise_hour = sprintf("%02d", $sunrise_hour);
 	$sunrise_min = sprintf("%02d", $sunrise_min);
 	$sunset_hour = sprintf("%02d", $sunset_hour);
 	$sunset_min = sprintf("%02d", $sunset_min);
	my $sunrise_value = "$sunrise_hour:$sunrise_min"; 
        my $sunset_value = "$sunset_hour:$sunset_min";
	my $sun_text = "Aube $sunrise_value Crépusc. $sunset_value";	
	
	#Take icon and make GD data
	# Create a new image
	my $im = new GD::Image(125, 60);
	my $x = 0;
	my $y = 0;

	my $imageTopLeft = GD::Image->newFromPng("$iconsdir/$city->{weather}{icon}.png");	
	#my $imageMoon = GD::Image->newFromPng("/root/bin/moon.png");	
	#my $imageTopLeft = GD::Image->newFromPng("/root/bin/50d.png");	
	
	# Allocate some colors
	my $white = $im->colorAllocate(255,255,255);
	my $black = $im->colorAllocate(0,0,0);
	my $gray1 = $im->colorAllocate(64,64,64);
	my $gray2 = $im->colorAllocate(128,128,128);

	# Make the background transparent and interlaced
	$im->transparent($white);
	$im->interlaced('true');
	
	#Merge Icon and Final image
	$im->copyMerge($imageTopLeft,-6,-12,0,0,50,50,100);
	#$im->copyMerge($imageMoon,48,0,0,0,20,20,100);

	my $rain_label = "R:";
	my $rain_value = undef;
	if ($city->{rain}{'3h'}){
		$rain_value = "$city->{rain}{'3h'}mn/3h";	
	} else {
		$rain_value = "0 mn/3h";
	}
	my $temperature_value = "".$temp."°C";
	my $humidity_label = "H:";
	my $humidity_value = "$city->{main}{humidity}%";
	my $pressure_label = "P:";
	my $pressure_value = "$city->{main}{pressure}hPa";
	my $line4 = "$city->{weather}{description} $city->{clouds}{all}%";
	my $line5 = "$wind_description $city->{wind}{speed}m/s";
	my $line6 = "$wind_direction_text $wind_direction°";
	#Fixe Latin1 for have sytange char on the picture
	$temperature_value = Encode::encode('latin1', $temperature_value);
	$humidity_value = Encode::encode('latin1', $humidity_value);

	$line4 = Encode::encode('latin1', $line4);
	$line5 = Encode::encode('latin1', $line5);
	$line6 = Encode::encode('latin1', $line6);
	$sun_text = Encode::encode('latin1', $sun_text);
	
	# Draw text in small font
	$im->string(gdGiantFont,$x+42, $y+0,       $temperature_value, $black);
	$im->string(gdTinyFont,$x+80,  $y+0,       $rain_label, $black);
	$im->string(gdTinyFont,$x+90,  $y+0,       $rain_value, $black);
        $im->string(gdTinyFont,$x+80,  $y+10,   $humidity_label, $black);
        $im->string(gdTinyFont,$x+90, $y+10,   $humidity_value, $black);
	$im->string(gdTinyFont,$x+80,  $y+20,   $pressure_label, $black);
        $im->string(gdTinyFont,$x+90, $y+20,   $pressure_value, $black);
        $im->string(gdTinyFont,$x, $y+29,   $line5, $black);
        $im->string(gdTinyFont,$x, $y+37,   $line6, $black);
	$im->string(gdTinyFont, $x,    $y+20+25, $line4, $black);
	$im->string(gdTinyFont, $x,    $y+20+33, $sun_text, $black);

	# Open a file for writing 
	open(PICTURE, ">picture.png") or die("Cannot open file for writing");

	# Make sure we are writing to a binary stream
	binmode PICTURE;

	# Convert the image to PNG and print it to the file PICTURE
	print PICTURE $im->png;
	close PICTURE;

}


__END__

=head1 NAME
sample - Using Getopt::Long and Pod::Usage
=head1 SYNOPSIS
sample [options] [file ...]
Options:
-help brief help message
-man full documentation
=head1 OPTIONS
=over 8
=item B<-help>
Print a brief help message and exits.
=item B<-man>
Prints the manual page and exits.
=back
=head1 DESCRIPTION
B<This program> will read the given input file(s) and do something
useful with the contents thereof.
=cut

