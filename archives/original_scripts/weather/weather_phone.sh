#! /bin/bash

DIR=/root/bin/weather
WWW_DIR=/var/www/galaxie.ici/phones/weather
CITY=guitrancourt
cd $DIR
$DIR/weather.pl --picture -c $CITY > $WWW_DIR/meteo.weather
if [ -f "$DIR/picture.png" ]
        then
	$DIR/img2cip.pl picture.png picture.cip && \
        rm $DIR/picture.png
fi
if [ -f "$DIR/picture.cip" ]
	then
	rsync $DIR/picture.cip $WWW_DIR/meteo.weather && \
	rm $DIR/picture.cip
fi
