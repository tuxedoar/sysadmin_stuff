#!/bin/bash 

# Postfix's queue checking and alerting by mail!.
# The 'swaks' tool is needed!.

QUEUE=$(/opt/zimbra/postfix/sbin/postqueue -p | grep empty; echo $? )
LOGS=$(/opt/zimbra/postfix/sbin/postqueue -p | tail -n 50)
THERESHOLD=300

if [ "$QUEUE" = 0 ]; then
  /usr/bin/logger "Postfix MONITOR: queue is empty. Nothing to do!."
else
  QUEUE_COUNTER=$(/opt/zimbra/postfix/sbin/postqueue -p | tail -1 | awk {'print $5'})
  if [ "$QUEUE_COUNTER" -gt "$THERESHOLD" ]; then
    /usr/bin/logger "Posfix ALERT: queue has suppassed current thereshold. Please check!!!\n\n"
    swaks --from someemail@something.com \
          --header "Subject: Postfix ALERT - there are $QUEUE_COUNTER messages in queue!!." \
          --header "X-Mailer: " \
          --body "Postfix ALERT - There are $QUEUE_COUNTER messages in queue!.\n\n LOGS:\n\n $LOGS" \
          --to adminone@something.com,admintwo@something.com \
          --server localhost
  else
    /usr/bin/logger "Postfix MONITOR: amount of queued messages is below $THERESHOLD !. Nothing to do!"
  fi
fi 
