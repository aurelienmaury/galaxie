#!/bin/bash
# Params:
#   $1 - dhclient.conf file path
#   $2 - configuration key to target
#   $3 - configuration value to add in the value list fo corresponding key
# Example:
#   dhclient_add.sh /etc/dhcp/dhclient.conf request domain-name
# Exit status:
#   0 - file modified
#   1 - file unchanged (either key absent or value already present)
#   2 - error (detected and throwed by sed)
sed  -r ":a;N;\$!ba; /\n$2([^;]|\n)*;/ {/\n$2([^;]|\n)*$3, ([^;]|\n)*;/ {s/\n($2([^;]|\n)*)($3, )(([^;]|\n)*);/\n\1\4;/g;q}};/\n$2([^;]|\n)*;/ {/\n$2([^;]|\n)*, $3;/ {s/\n($2([^;]|\n)*)(, $3;)/\n\1;/g;q}};q1" -i $1
