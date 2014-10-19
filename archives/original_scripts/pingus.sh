#!/bin/bash
exec 2>&1
DBDIR=/usr/local/dlog/dbs
case $1 in (create)
#--step 300 \
/usr/bin/rrdtool create $DBDIR/ping_wan.rrd \
--step 60 \
DS:pl:GAUGE:600:0:100 \
DS:rtt:GAUGE:600:0:10000000 \
RRA:AVERAGE:0.5:1:800 \
RRA:AVERAGE:0.5:6:800 \
RRA:AVERAGE:0.5:24:800 \
RRA:AVERAGE:0.5:288:800 \
RRA:MAX:0.5:1:800 \
RRA:MAX:0.5:6:800 \
RRA:MAX:0.5:24:800 \
RRA:MAX:0.5:288:800;;
	(update)
                PING=/bin/ping
                COUNT=4
                DEADLINE=10
		output=$($PING -q -n -c $COUNT -w $DEADLINE ovh.fr 2>&1)
		# notice $output is quoted to preserve newlines
		temp=$(echo "$output"| awk '
        BEGIN           {pl=100; rtt=0.1}
        /packets transmitted/   {
            match($0, /([0-9]+)% packet loss/, matchstr)
            pl=matchstr[1]
        }
        /^rtt/          {
            # looking for something like 0.562/0.566/0.571/0.024
            match($4, /(.*)\/(.*)\/(.*)\/(.*)/, a)
            rtt=a[2]
        }
        /unknown host/  {
            # no output at all means network is probably down
            pl=100
            rtt=0.1
        }
        END             {print pl ":" rtt}
        ')
    	RETURN_VALUE=$temp
	/usr/bin/rrdtool update $DBDIR/ping_wan.rrd --template pl:rtt N:$RETURN_VALUE;;
	(graph)
cd /var/www/galaxie.ici/ping
echo "
<HTML>
<HEAD><TITLE>Round-Trip and Packet Loss Stats</TITLE></HEAD>
<BODY>
<H3>Hourly Round-Trip & Packetloss Stats(1min average)</H3>
" > ping.html
rrdtool graph ping_wan_hour.png -h 300 -w 700 -a PNG \
--imginfo '<IMG SRC=/stats/%s WIDTH=%lu HEIGHT=%lu >' \
--lazy --start -3600 --end -60 --x-grid MINUTE:10:HOUR:1:MINUTE:30:0:%R \
-v "Packet Lost" -t "Lantency vers ovh.fr - `/bin/date`" \
--rigid \
--lower-limit 0 \
DEF:roundtrip=$DBDIR/ping_wan.rrd:rtt:AVERAGE \
DEF:packetloss=$DBDIR/ping_wan.rrd:pl:AVERAGE \
CDEF:PLNone=packetloss,0,1,LIMIT,UN,UNKN,INF,IF \
CDEF:PL1=packetloss,1,2,LIMIT,UN,UNKN,INF,IF \
CDEF:PL2=packetloss,2,3,LIMIT,UN,UNKN,INF,IF \
CDEF:PL3=packetloss,3,4,LIMIT,UN,UNKN,INF,IF \
CDEF:PL4=packetloss,4,5,LIMIT,UN,UNKN,INF,IF \
CDEF:PL5=packetloss,5,6,LIMIT,UN,UNKN,INF,IF \
CDEF:PL6=packetloss,6,7,LIMIT,UN,UNKN,INF,IF \
CDEF:PL7=packetloss,7,8,LIMIT,UN,UNKN,INF,IF \
CDEF:PL8=packetloss,8,9,LIMIT,UN,UNKN,INF,IF \
CDEF:PL9=packetloss,9,10,LIMIT,UN,UNKN,INF,IF \
CDEF:PL10=packetloss,10,11,LIMIT,UN,UNKN,INF,IF \
CDEF:PL11=packetloss,11,12,LIMIT,UN,UNKN,INF,IF \
CDEF:PL12=packetloss,12,13,LIMIT,UN,UNKN,INF,IF \
CDEF:PL13=packetloss,13,14,LIMIT,UN,UNKN,INF,IF \
CDEF:PL14=packetloss,14,15,LIMIT,UN,UNKN,INF,IF \
CDEF:PL15=packetloss,15,16,LIMIT,UN,UNKN,INF,IF \
CDEF:PL25=packetloss,16,25,LIMIT,UN,UNKN,INF,IF \
CDEF:PL50=packetloss,25,50,LIMIT,UN,UNKN,INF,IF \
CDEF:PL75=packetloss,50,75,LIMIT,UN,UNKN,INF,IF \
CDEF:PL100=packetloss,75,100,LIMIT,UN,UNKN,INF,IF \
AREA:roundtrip#4444ff:"Round Trip Time (millis)" \
GPRINT:roundtrip:LAST:"Cur\: %5.2lf ms" \
GPRINT:roundtrip:AVERAGE:"Avg\: %5.2lf ms" \
GPRINT:roundtrip:MAX:"Max\: %5.2lf ms" \
GPRINT:roundtrip:MIN:"Min\: %5.2lfms \n" \
COMMENT:"Packet Loss Percentage \n" \
AREA:PLNone#00FF00:"0%":STACK \
AREA:PL1#EEFF00:"1%":STACK \
AREA:PL2#FFFF00:"2%":STACK \
AREA:PL3#FFEE00:"3%":STACK \
AREA:PL4#FFDD00:"4%":STACK \
AREA:PL5#FFCC00:"5%":STACK \
AREA:PL6#FFBB00:"6%":STACK \
AREA:PL7#FFAA00:"7%":STACK \
AREA:PL8#FF9900:"8%":STACK \
AREA:PL9#FF8800:"9%":STACK \
AREA:PL10#FF7700:"10%":STACK \
AREA:PL11#FF6600:"11%":STACK \
AREA:PL12#FF5500:"12%":STACK \
AREA:PL13#FF4400:"13%":STACK \
AREA:PL14#FF3300:"14%":STACK \
AREA:PL15#FF2200:"15%":STACK \
AREA:PL25#FF1100:"15-25%":STACK \
AREA:PL50#FF0000:"25-50%":STACK \
AREA:PL75#FF0000:"50-75%":STACK \
AREA:PL100#FF0000:"75-100%":STACK
echo "
<img src="ping_wan_hour.png"><br>
<br>
<H3>Daily Round-Trip & Packetloss Stats(1min average)</H3>
" >> ping.html
rrdtool graph ping_wan_day.png -h 300 -w 700 -a PNG \
--imginfo '<IMG SRC=/stats/%s WIDTH=%lu HEIGHT=%lu >' \
--lazy --start -86400 --end -60 --x-grid MINUTE:30:HOUR:1:HOUR:2:0:%H \
-v "Round-Trip Time (ms)" -t "Lantency vers ovh.fr - `/bin/date`" \
--rigid \
--lower-limit 0 \
DEF:roundtrip=$DBDIR/ping_wan.rrd:rtt:AVERAGE \
DEF:packetloss=$DBDIR/ping_wan.rrd:pl:AVERAGE \
CDEF:PLNone=packetloss,0,1,LIMIT,UN,UNKN,INF,IF \
CDEF:PL1=packetloss,1,2,LIMIT,UN,UNKN,INF,IF \
CDEF:PL2=packetloss,2,3,LIMIT,UN,UNKN,INF,IF \
CDEF:PL3=packetloss,3,4,LIMIT,UN,UNKN,INF,IF \
CDEF:PL4=packetloss,4,5,LIMIT,UN,UNKN,INF,IF \
CDEF:PL5=packetloss,5,6,LIMIT,UN,UNKN,INF,IF \
CDEF:PL6=packetloss,6,7,LIMIT,UN,UNKN,INF,IF \
CDEF:PL7=packetloss,7,8,LIMIT,UN,UNKN,INF,IF \
CDEF:PL8=packetloss,8,9,LIMIT,UN,UNKN,INF,IF \
CDEF:PL9=packetloss,9,10,LIMIT,UN,UNKN,INF,IF \
CDEF:PL10=packetloss,10,11,LIMIT,UN,UNKN,INF,IF \
CDEF:PL11=packetloss,11,12,LIMIT,UN,UNKN,INF,IF \
CDEF:PL12=packetloss,12,13,LIMIT,UN,UNKN,INF,IF \
CDEF:PL13=packetloss,13,14,LIMIT,UN,UNKN,INF,IF \
CDEF:PL14=packetloss,14,15,LIMIT,UN,UNKN,INF,IF \
CDEF:PL15=packetloss,15,16,LIMIT,UN,UNKN,INF,IF \
CDEF:PL25=packetloss,16,25,LIMIT,UN,UNKN,INF,IF \
CDEF:PL50=packetloss,25,50,LIMIT,UN,UNKN,INF,IF \
CDEF:PL75=packetloss,50,75,LIMIT,UN,UNKN,INF,IF \
CDEF:PL100=packetloss,75,100,LIMIT,UN,UNKN,INF,IF \
AREA:roundtrip#4444ff:"Round Trip Time (millis)" \
GPRINT:roundtrip:LAST:"Cur\: %5.2lf ms" \
GPRINT:roundtrip:AVERAGE:"Avg\: %5.2lf ms" \
GPRINT:roundtrip:MAX:"Max\: %5.2lf ms" \
GPRINT:roundtrip:MIN:"Min\: %5.2lfms \n" \
COMMENT:"Packet Loss Percentage \n" \
AREA:PLNone#00FF00:"0%":STACK \
AREA:PL1#EEFF00:"1%":STACK \
AREA:PL2#FFFF00:"2%":STACK \
AREA:PL3#FFEE00:"3%":STACK \
AREA:PL4#FFDD00:"4%":STACK \
AREA:PL5#FFCC00:"5%":STACK \
AREA:PL6#FFBB00:"6%":STACK \
AREA:PL7#FFAA00:"7%":STACK \
AREA:PL8#FF9900:"8%":STACK \
AREA:PL9#FF8800:"9%":STACK \
AREA:PL10#FF7700:"10%":STACK \
AREA:PL11#FF6600:"11%":STACK \
AREA:PL12#FF5500:"12%":STACK \
AREA:PL13#FF4400:"13%":STACK \
AREA:PL14#FF3300:"14%":STACK \
AREA:PL15#FF2200:"15%":STACK \
AREA:PL25#FF1100:"15-25%":STACK \
AREA:PL50#FF0000:"25-50%":STACK \
AREA:PL75#FF0000:"50-75%":STACK \
AREA:PL100#FF0000:"75-100%":STACK
echo "
<img src="ping_wan_day.png"><br>
<br>
<H3>Weekly Round-Trip & Packetloss Stats(1min average)</H3>
" >> ping.html
rrdtool graph ping_wan_week.png -h 300 -w 700 -a PNG \
--imginfo '<IMG SRC=/stats/%s WIDTH=%lu HEIGHT=%lu >' \
--lazy --start -604800 --end -1800 \
-v "Round-Trip Time (ms)" -t "Lantency vers ovh.fr - `/bin/date`" \
--rigid \
--lower-limit 0 \
DEF:roundtrip=$DBDIR/ping_wan.rrd:rtt:AVERAGE \
DEF:packetloss=$DBDIR/ping_wan.rrd:pl:AVERAGE \
CDEF:PLNone=packetloss,0,1,LIMIT,UN,UNKN,INF,IF \
CDEF:PL1=packetloss,1,2,LIMIT,UN,UNKN,INF,IF \
CDEF:PL2=packetloss,2,3,LIMIT,UN,UNKN,INF,IF \
CDEF:PL3=packetloss,3,4,LIMIT,UN,UNKN,INF,IF \
CDEF:PL4=packetloss,4,5,LIMIT,UN,UNKN,INF,IF \
CDEF:PL5=packetloss,5,6,LIMIT,UN,UNKN,INF,IF \
CDEF:PL6=packetloss,6,7,LIMIT,UN,UNKN,INF,IF \
CDEF:PL7=packetloss,7,8,LIMIT,UN,UNKN,INF,IF \
CDEF:PL8=packetloss,8,9,LIMIT,UN,UNKN,INF,IF \
CDEF:PL9=packetloss,9,10,LIMIT,UN,UNKN,INF,IF \
CDEF:PL10=packetloss,10,11,LIMIT,UN,UNKN,INF,IF \
CDEF:PL11=packetloss,11,12,LIMIT,UN,UNKN,INF,IF \
CDEF:PL12=packetloss,12,13,LIMIT,UN,UNKN,INF,IF \
CDEF:PL13=packetloss,13,14,LIMIT,UN,UNKN,INF,IF \
CDEF:PL14=packetloss,14,15,LIMIT,UN,UNKN,INF,IF \
CDEF:PL15=packetloss,15,16,LIMIT,UN,UNKN,INF,IF \
CDEF:PL25=packetloss,16,25,LIMIT,UN,UNKN,INF,IF \
CDEF:PL50=packetloss,25,50,LIMIT,UN,UNKN,INF,IF \
CDEF:PL75=packetloss,50,75,LIMIT,UN,UNKN,INF,IF \
CDEF:PL100=packetloss,75,100,LIMIT,UN,UNKN,INF,IF \
AREA:roundtrip#4444ff:"Round Trip Time (millis)" \
GPRINT:roundtrip:LAST:"Cur\: %5.2lf ms" \
GPRINT:roundtrip:AVERAGE:"Avg\: %5.2lf ms" \
GPRINT:roundtrip:MAX:"Max\: %5.2lf ms" \
GPRINT:roundtrip:MIN:"Min\: %5.2lfms \n" \
COMMENT:"Packet Loss Percentage \n" \
AREA:PLNone#00FF00:"0%":STACK \
AREA:PL1#EEFF00:"1%":STACK \
AREA:PL2#FFFF00:"2%":STACK \
AREA:PL3#FFEE00:"3%":STACK \
AREA:PL4#FFDD00:"4%":STACK \
AREA:PL5#FFCC00:"5%":STACK \
AREA:PL6#FFBB00:"6%":STACK \
AREA:PL7#FFAA00:"7%":STACK \
AREA:PL8#FF9900:"8%":STACK \
AREA:PL9#FF8800:"9%":STACK \
AREA:PL10#FF7700:"10%":STACK \
AREA:PL11#FF6600:"11%":STACK \
AREA:PL12#FF5500:"12%":STACK \
AREA:PL13#FF4400:"13%":STACK \
AREA:PL14#FF3300:"14%":STACK \
AREA:PL15#FF2200:"15%":STACK \
AREA:PL25#FF1100:"15-25%":STACK \
AREA:PL50#FF0000:"25-50%":STACK \
AREA:PL75#FF0000:"50-75%":STACK \
AREA:PL100#FF0000:"75-100%":STACK
echo "
<img src="ping_wan_week.png"><br>
<br>
<H3>Monthly Round-Trip & Packetloss Stats(1min average)</H3>
" >> ping.html
rrdtool graph ping_wan_month.png -h 300 -w 700 -a PNG \
--imginfo '<IMG SRC=/stats/%s WIDTH=%lu HEIGHT=%lu >' \
--lazy --start -2592000 --end -7200 \
-v "Round-Trip Time (ms)" -t "Lantency vers ovh.fr - `/bin/date`" \
--rigid \
--lower-limit 0 \
DEF:roundtrip=$DBDIR/ping_wan.rrd:rtt:AVERAGE \
DEF:packetloss=$DBDIR/ping_wan.rrd:pl:AVERAGE \
CDEF:PLNone=packetloss,0,1,LIMIT,UN,UNKN,INF,IF \
CDEF:PL1=packetloss,1,2,LIMIT,UN,UNKN,INF,IF \
CDEF:PL2=packetloss,2,3,LIMIT,UN,UNKN,INF,IF \
CDEF:PL3=packetloss,3,4,LIMIT,UN,UNKN,INF,IF \
CDEF:PL4=packetloss,4,5,LIMIT,UN,UNKN,INF,IF \
CDEF:PL5=packetloss,5,6,LIMIT,UN,UNKN,INF,IF \
CDEF:PL6=packetloss,6,7,LIMIT,UN,UNKN,INF,IF \
CDEF:PL7=packetloss,7,8,LIMIT,UN,UNKN,INF,IF \
CDEF:PL8=packetloss,8,9,LIMIT,UN,UNKN,INF,IF \
CDEF:PL9=packetloss,9,10,LIMIT,UN,UNKN,INF,IF \
CDEF:PL10=packetloss,10,11,LIMIT,UN,UNKN,INF,IF \
CDEF:PL11=packetloss,11,12,LIMIT,UN,UNKN,INF,IF \
CDEF:PL12=packetloss,12,13,LIMIT,UN,UNKN,INF,IF \
CDEF:PL13=packetloss,13,14,LIMIT,UN,UNKN,INF,IF \
CDEF:PL14=packetloss,14,15,LIMIT,UN,UNKN,INF,IF \
CDEF:PL15=packetloss,15,16,LIMIT,UN,UNKN,INF,IF \
CDEF:PL25=packetloss,16,25,LIMIT,UN,UNKN,INF,IF \
CDEF:PL50=packetloss,25,50,LIMIT,UN,UNKN,INF,IF \
CDEF:PL75=packetloss,50,75,LIMIT,UN,UNKN,INF,IF \
CDEF:PL100=packetloss,75,100,LIMIT,UN,UNKN,INF,IF \
AREA:roundtrip#4444ff:"Round Trip Time (millis)" \
GPRINT:roundtrip:LAST:"Cur\: %5.2lf ms" \
GPRINT:roundtrip:AVERAGE:"Avg\: %5.2lf ms" \
GPRINT:roundtrip:MAX:"Max\: %5.2lf ms" \
GPRINT:roundtrip:MIN:"Min\: %5.2lfms \n" \
COMMENT:"Packet Loss Percentage \n" \
AREA:PLNone#00FF00:"0%":STACK \
AREA:PL1#EEFF00:"1%":STACK \
AREA:PL2#FFFF00:"2%":STACK \
AREA:PL3#FFEE00:"3%":STACK \
AREA:PL4#FFDD00:"4%":STACK \
AREA:PL5#FFCC00:"5%":STACK \
AREA:PL6#FFBB00:"6%":STACK \
AREA:PL7#FFAA00:"7%":STACK \
AREA:PL8#FF9900:"8%":STACK \
AREA:PL9#FF8800:"9%":STACK \
AREA:PL10#FF7700:"10%":STACK \
AREA:PL11#FF6600:"11%":STACK \
AREA:PL12#FF5500:"12%":STACK \
AREA:PL13#FF4400:"13%":STACK \
AREA:PL14#FF3300:"14%":STACK \
AREA:PL15#FF2200:"15%":STACK \
AREA:PL25#FF1100:"15-25%":STACK \
AREA:PL50#FF0000:"25-50%":STACK \
AREA:PL75#FF0000:"50-75%":STACK \
AREA:PL100#FF0000:"75-100%":STACK
echo "
<img src="ping_wan_month.png"><br>
<br>
<H3>Yearly Round-Trip & Packetloss Stats(1min average)</H3>
" >> ping.html
rrdtool graph ping_wan_year.png \
--imginfo '<IMG SRC=/stats/%s WIDTH=%lu HEIGHT=%lu >' \
--lazy --start -31536000 --end -86400 -h 300 -w 700 -a PNG \
-v "Round-Trip Time (ms)" -t "Lantency vers ovh.fr - `/bin/date`" \
--rigid \
--lower-limit 0 \
DEF:roundtrip=$DBDIR/ping_wan.rrd:rtt:AVERAGE \
DEF:packetloss=$DBDIR/ping_wan.rrd:pl:AVERAGE \
CDEF:PLNone=packetloss,0,1,LIMIT,UN,UNKN,INF,IF \
CDEF:PL1=packetloss,1,2,LIMIT,UN,UNKN,INF,IF \
CDEF:PL2=packetloss,2,3,LIMIT,UN,UNKN,INF,IF \
CDEF:PL3=packetloss,3,4,LIMIT,UN,UNKN,INF,IF \
CDEF:PL4=packetloss,4,5,LIMIT,UN,UNKN,INF,IF \
CDEF:PL5=packetloss,5,6,LIMIT,UN,UNKN,INF,IF \
CDEF:PL6=packetloss,6,7,LIMIT,UN,UNKN,INF,IF \
CDEF:PL7=packetloss,7,8,LIMIT,UN,UNKN,INF,IF \
CDEF:PL8=packetloss,8,9,LIMIT,UN,UNKN,INF,IF \
CDEF:PL9=packetloss,9,10,LIMIT,UN,UNKN,INF,IF \
CDEF:PL10=packetloss,10,11,LIMIT,UN,UNKN,INF,IF \
CDEF:PL11=packetloss,11,12,LIMIT,UN,UNKN,INF,IF \
CDEF:PL12=packetloss,12,13,LIMIT,UN,UNKN,INF,IF \
CDEF:PL13=packetloss,13,14,LIMIT,UN,UNKN,INF,IF \
CDEF:PL14=packetloss,14,15,LIMIT,UN,UNKN,INF,IF \
CDEF:PL15=packetloss,15,16,LIMIT,UN,UNKN,INF,IF \
CDEF:PL25=packetloss,16,25,LIMIT,UN,UNKN,INF,IF \
CDEF:PL50=packetloss,25,50,LIMIT,UN,UNKN,INF,IF \
CDEF:PL75=packetloss,50,75,LIMIT,UN,UNKN,INF,IF \
CDEF:PL100=packetloss,75,100,LIMIT,UN,UNKN,INF,IF \
AREA:roundtrip#4444ff:"Round Trip Time (millis)" \
GPRINT:roundtrip:LAST:"Cur\: %5.2lf ms" \
GPRINT:roundtrip:AVERAGE:"Avg\: %5.2lf ms" \
GPRINT:roundtrip:MAX:"Max\: %5.2lf ms" \
GPRINT:roundtrip:MIN:"Min\: %5.2lfms \n" \
COMMENT:"Packet Loss Percentage \n" \
AREA:PLNone#00FF00:"0%":STACK \
AREA:PL1#EEFF00:"1%":STACK \
AREA:PL2#FFFF00:"2%":STACK \
AREA:PL3#FFEE00:"3%":STACK \
AREA:PL4#FFDD00:"4%":STACK \
AREA:PL5#FFCC00:"5%":STACK \
AREA:PL6#FFBB00:"6%":STACK \
AREA:PL7#FFAA00:"7%":STACK \
AREA:PL8#FF9900:"8%":STACK \
AREA:PL9#FF8800:"9%":STACK \
AREA:PL10#FF7700:"10%":STACK \
AREA:PL11#FF6600:"11%":STACK \
AREA:PL12#FF5500:"12%":STACK \
AREA:PL13#FF4400:"13%":STACK \
AREA:PL14#FF3300:"14%":STACK \
AREA:PL15#FF2200:"15%":STACK \
AREA:PL25#FF1100:"15-25%":STACK \
AREA:PL50#FF0000:"25-50%":STACK \
AREA:PL75#FF0000:"50-75%":STACK \
AREA:PL100#FF0000:"75-100%":STACK
echo "
<img src="ping_wan_year.png"><br>
<br>
</BODY>
</HTML>
" >> ping.html
;;
esac
