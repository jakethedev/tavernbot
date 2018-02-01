#!/bin/bash
PATH="$PATH:/user/bin"
LOCK='./daemon.lock'
LOG='./pidaemon.log'

# Check for a nodemon process, and if there isn't one, run it
if [[ -f $LOCK ]]; then
  echo "$(date): WARN Already summoning!" >> $LOG
else
  touch $LOCK
  pgrep node -a || absent=true
  if [[ $absent ]]; then
    echo "$(date): WARN No nodemon found, summoning..." >> $LOG
    npm run daemon >> $LOG &
  else
    echo "$(date): OK Running as expected" >> $LOG
  fi
  rm $LOCK
fi
