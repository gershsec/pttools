#!/bin/zsh
# Keychain password fetch by gershsec
# v1.0

# argument check 
if [ $# -ne 2 ]; then
  echo "Usage: $0 <keychain_name> <user_account>"
  exit 1
fi

KEYCHAIN_NAME=$1
USER_ACCOUNT=$2

# retrieve password for specified user in specified keychain 
PASSWORD=$(security find-generic-password -a "$USER_ACCOUNT" -w "$KEYCHAIN_NAME".keychain-db)

# copy password to clipboard  
if [ $? -eq 0 ]; then
  echo -n $PASSWORD | pbcopy
else
  echo "Error: Unable to retrieve password for $USER_ACCOUNT from $KEYCHAIN_NAME."
  exit 1
fi
