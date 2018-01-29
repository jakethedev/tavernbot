#!/bin/bash
PATH="$PATH:/user/bin"

# Check for a nodemon process, and if there isn't one, run it
pgrep node -a || absent=true
if [[ $absent ]]; then
  echo "No nodemon found, summoning..."
  npm run daemon &
else
  echo "Running as expected"
fi
