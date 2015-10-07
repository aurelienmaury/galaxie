#!/bin/sh

ORIG=$(pwd)
URL=$1

ARCHIVE="$(echo "$URL" | rev | cut -d"/" -f1 | rev)"

wget -O /tmp/$ARCHIVE $URL

cd /tmp && tar xvzf $ARCHIVE

DIRECTORY="$(echo "$ARCHIVE" | cut -d"." -f1 )"

cd /tmp/$DIRECTORY

DATE="$(date +%Y%m%d%H%M)"
mkdir $ORIG/training-$DATE

sed -e "s/\([^ ]*\) \(.*\)/\2 (\1)/g" /tmp/$DIRECTORY/etc/prompts-original  \
    | tr '[:upper:]' '[:lower:]' \
    | sed -e "s/[’]/'/g" \
    | sed -e "s/[']/' /g" \
    | sed -e "s/[.,«»:]/ /g" \
    | tr "/" " " \
    | tr -s " " > $ORIG/training-$DATE/transcription

cp /tmp/$DIRECTORY/wav/*.wav $ORIG/training-$DATE


echo .
echo "./train.sh \$(pwd)/audio-profile-current fr-fr $ORIG/training-$DATE"
echo .