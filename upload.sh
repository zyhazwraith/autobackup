#!/bin/bash


WORKSPACE=$(dirname "$(readlink -f $0)")
DIR=$1
FILES=$(date +%Y%m%d)_${1##*/}
TOKEN=$(cat $WORKSPACE/token | grep -e "\bTOKEN\b" | awk -F '=' '{print $2}')
TOKEN_SECRET=$(cat $WORKSPACE/token | grep -e "\bTOKEN_SECRET\b" | awk -F '=' '{print $2}')

#echo $TOKEN $TOKEN_SECRET
#echo $FILES

echo $WORKSPACE $DIR $FILES  >> /home/zzz/cron
tar -jcpf $WORKSPACE/"$FILES".tar.gz2 $DIR 2>/dev/null
$WORKSPACE/upload.py "$FILES".tar.gz2 $TOKEN $TOKEN_SECRET
rm $WORKSPACE/"$FILES".tar.gz2

exit 0
