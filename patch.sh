#!/bin/bash

LOGIN_DESTINATION_FILE="login.py"
ACCOUNTS_POOL_DESTINATION_FILE="accounts_pool.py"
DESTINATION_DIR="./venv/lib/python3.10/site-packages/twscrape"
LOGIN_DESTINATION_PATH="$DESTINATION_DIR/$LOGIN_DESTINATION_FILE"
ACCOUNTS_POOL_DESTINATION_PATH="$DESTINATION_DIR/$ACCOUNTS_POOL_DESTINATION_FILE"
PATCH_DIR="./patch"
LOGIN_PATCH_FILE="$PATCH_DIR/login_patch.py"
ACCOUNTS_POOL_PATCH_FILE="$PATCH_DIR/accounts_pool_patch.py"

if [ ! -f "$LOGIN_PATCH_FILE" ]; then
    echo "Error: Source login patch file does not exist."
fi

if [ ! -f "$ACCOUNTS_POOL_PATCH_FILE" ]; then
    echo "Error: Source accounts_pool patch file does not exist."
fi

if [ -f "$LOGIN_DESTINATION_PATH" ]; then
    rm "$LOGIN_DESTINATION_PATH"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to remove the existing login destination file."
    fi
fi

if [ -f "$ACCOUNTS_POOL_DESTINATION_PATH" ]; then
    rm "$ACCOUNTS_POOL_DESTINATION_PATH"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to remove the existing accounts_pool destination file."
    fi
fi

cp "$LOGIN_PATCH_FILE" "$LOGIN_DESTINATION_PATH"
cp "$ACCOUNTS_POOL_PATCH_FILE" "$ACCOUNTS_POOL_DESTINATION_PATH"

if [ $? -eq 0 ]; then
    echo "twscrape Library patch success"
else
    echo "Error: Failed to patch twscrape Library"
fi