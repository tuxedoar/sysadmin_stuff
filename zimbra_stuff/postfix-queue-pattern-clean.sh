#!/bin/bash

# Clean Postfix queued messages that matches an specific pattern!. 

TARGET="some_pattern"
ID=$(/opt/zimbra/postfix/sbin/postqueue -p | grep -i $TARGET  | awk '{ print $1 }' | grep -oP '(([A-Z]{1})|([0-9]{1})){12}')

for i in $ID; do
  /opt/zimbra/postfix/sbin/postsuper -d $i
done
