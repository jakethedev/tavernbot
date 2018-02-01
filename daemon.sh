#!/bin/bash
PATH="$PATH:/user/bin"
LOCK='./daemon.lock'

# Check for a nodemon process, and if there isn't one, run it
if [[ -f $LOCK ]]; then
  echo "$(date): WARN Already summoning!"
else
  touch $LOCK
  pgrep node -a || absent=true
  if [[ $absent ]]; then
    echo "$(date): WARN No nodemon found, summoning..."
    npm run daemon > pidaemon.log &
  else
    echo "$(date): OK Running as expected"
  fi
  rm $LOCK
fi
