#!/bin/bash

# Set the environment variable in your .bashrc file like so:
# export PUSHBULLET_API="MY_PUSHBULLET_API_KEY"
MSG="$1"

curl -u $PUSHBULLET_API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Alert" -d body="$MSG"
