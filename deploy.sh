#!/usr/bin/env bash

WORKING_DIRECTORY="~/www/cs1531_deploy"

USERNAME="magicant"
SSH_HOST="ssh-magicant.alwaysdata.net"

rm -rf ./**/__pycache__ ./**/.pytest_cache > /dev/null
rm -f ./src/_data.json

ssh "$USERNAME@$SSH_HOST" "rm -r -f $WORKING_DIRECTORY/src"
scp -r ./src "$USERNAME@$SSH_HOST:$WORKING_DIRECTORY"
# ssh "$USERNAME@$SSH_HOST" "cd $WORKING_DIRECTORY && source env/bin/activate && pip3 install -r requirements.txt"
