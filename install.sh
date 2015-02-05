#!/bin/bash

./access.py

DIR=$(pwd)
echo "$(crontab -l)" >cron
echo "* * * * * cat $DIR/token | grep -e \"\\bFOLDERS\\b\" | awk -F '=' '{print \$2}' | awk -F ';' '{for(i=1; i<NF; i++) system(\"$DIR/upload.sh \"\$i) }'" >>cron
crontab cron
rm cron

exit 0
