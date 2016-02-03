#! /bin/bash
URL=$1
MOTIF="  Location:"
wget --server-response --spider "$URL" 2>&1 | grep "$MOTIF" | awk -F/ '{print $NF}'