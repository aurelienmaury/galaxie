#! /bin/bash
#URL="https://download.mozilla.org/?product=thunderbird-latest&os=linux64&lang=fr"
URL=$1
MOTIF="  Location:"
wget --server-response --spider "$URL" 2>&1 | grep "$MOTIF" | awk -F/ '{print $NF}'