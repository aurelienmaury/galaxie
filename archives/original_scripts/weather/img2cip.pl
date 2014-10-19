#!/usr/bin/perl
# Convert a png to a cip

use strict;
use GD;
use IO::File;

die "Usage: $0 <in file> <out file>\n"
    unless @ARGV == 2;

my $in = GD::Image->new($ARGV[0]);
my ($width, $height) = $in->getBounds;

my @data;
for (my $y = 0; $y < $height; $y++)
{
    for (my $x = 0; $x < $width; $x++)
    {
	my $color = $in->getPixel($x, $y);
	my ($r, $g, $b) = $in->rgb($color);
	$r /= 255;
	$g /= 255;
	$b /= 255;
	my $intense = .299*$r + .587*$g + .114*$b;
	if ($intense < .25)
	{
	    push @data, 3;
	}
	elsif ($intense < .5)
	{
	    push @data, 2;
	}
	elsif ($intense < .75)
	{
	    push @data, 1;
	}
	else
	{
	    push @data, 0;
	}
    }
}

# Collapse into hex
my @hex_data;
for (my $i = 0; $i < @data; $i+=4)
{
    push @hex_data, sprintf("%X", $data[$i+2]+4*$data[$i+3]);
    push @hex_data, sprintf("%X", $data[$i]+4*$data[$i+1]);
}

my $out = new IO::File ">$ARGV[1]";
print $out "<CiscoIPPhoneImage>\n";
print $out "  <Title/>\n";
print $out "   <LocationX>-1</LocationX>\n";
print $out "   <LocationY>-1</LocationY>\n";
print $out "   <Width>$width</Width>\n";
print $out "   <Height>$height</Height>\n";
print $out "   <Depth>2</Depth>\n";
print $out "   <Data>";
print $out @hex_data;
print $out "</Data>\n";
print $out "   <Prompt/>\n";
print $out "</CiscoIPPhoneImage>\n";
$out->close;
