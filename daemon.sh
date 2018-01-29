#!/bin/bash
PATH="$PATH:/user/bin"

# Check for a nodemon process, and if there isn't one, run it
pgrep node -a || absent=true
if [[ $absent ]]; then
  echo "$(date): WARN No nodemon found, summoning..."
  npm run daemon &
else
  echo "$(date): OK Running as expected"
fi
