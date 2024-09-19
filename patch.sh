#!/bin/bash

LOGIN_DESTINATION_FILE="login.py"
ACCOUNTS_POOL_DESTINATION_FILE="accounts_pool.py"
DB_DESTINATION_FILE="db.py"
ACCOUNT_DESTINATION_FILE="account.py"

DESTINATION_DIR="./venv/lib/python3.10/site-packages/twscrape"
LOGIN_DESTINATION_PATH="$DESTINATION_DIR/$LOGIN_DESTINATION_FILE"
ACCOUNTS_POOL_DESTINATION_PATH="$DESTINATION_DIR/$ACCOUNTS_POOL_DESTINATION_FILE"
DB_DESTINATION_PATH="$DESTINATION_DIR/$DB_DESTINATION_FILE"
ACCOUNT_DESTINATION_PATH="$DESTINATION_DIR/$ACCOUNT_DESTINATION_FILE"

PATCH_DIR="./patch"
LOGIN_PATCH_FILE="$PATCH_DIR/login_patch.py"
ACCOUNTS_POOL_PATCH_FILE="$PATCH_DIR/accounts_pool_patch.py"
DB_PATCH_FILE="$PATCH_DIR/db_patch.py"
ACCOUNT_PATCH_FILE="$PATCH_DIR/account_patch.py"

# if [ $# -eq 0 ]; then
#     echo "Usage: $0 {login|accounts_pool|db|account|all}"
# fi

patch_login() {
    if [ ! -f "$LOGIN_PATCH_FILE" ]; then
        echo "Error: Source login patch file does not exist."
        return
    fi

    if [ -f "$LOGIN_DESTINATION_PATH" ]; then
        rm "$LOGIN_DESTINATION_PATH"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to remove the existing login destination file."
            return
        fi
    fi

    cp "$LOGIN_PATCH_FILE" "$LOGIN_DESTINATION_PATH"
    if [ $? -eq 0 ]; then
        echo "twscrape Library login patch success"
    else
        echo "Error: Failed to patch login.py"
    fi
}

patch_accounts_pool() {
    if [ ! -f "$ACCOUNTS_POOL_PATCH_FILE" ];then
        echo "Error: Source accounts_pool patch file does not exist."
        return
    fi

    if [ -f "$ACCOUNTS_POOL_DESTINATION_PATH" ]; then
        rm "$ACCOUNTS_POOL_DESTINATION_PATH"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to remove the existing accounts_pool destination file."
            return
        fi
    fi

    cp "$ACCOUNTS_POOL_PATCH_FILE" "$ACCOUNTS_POOL_DESTINATION_PATH"
    if [ $? -eq 0 ]; then
        echo "twscrape Library accounts_pool patch success"
    else
        echo "Error: Failed to patch accounts_pool.py"
    fi
}

patch_db() {
    if [ ! -f "$DB_PATCH_FILE" ]; then
        echo "Error: Source db patch file does not exist."
        return
    fi

    if [ -f "$DB_DESTINATION_PATH" ]; then
        rm "$DB_DESTINATION_PATH"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to remove the existing db destination file."
            return
        fi
    fi

    cp "$DB_PATCH_FILE" "$DB_DESTINATION_PATH"
    if [ $? -eq 0 ]; then
        echo "twscrape Library db patch success"
    else
        echo "Error: Failed to patch db.py"
    fi
}

patch_account() {
    if [ ! -f "$ACCOUNT_PATCH_FILE" ]; then
        echo "Error: Source account patch file does not exist."
        return
    fi

    if [ -f "$ACCOUNT_DESTINATION_PATH" ]; then
        rm "$ACCOUNT_DESTINATION_PATH"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to remove the existing account destination file."
            return
        fi
    fi

    cp "$ACCOUNT_PATCH_FILE" "$ACCOUNT_DESTINATION_PATH"
    if [ $? -eq 0 ]; then
        echo "twscrape Library account patch success"
    else
        echo "Error: Failed to patch account.py"
    fi
}

patch_login
patch_accounts_pool
patch_db
patch_account

# case $1 in
#     login)
#         patch_login
#         ;;
#     accounts_pool)
#         patch_accounts_pool
#         ;;
#     db)
#         patch_db
#         ;;
#     account)
#         patch_account
#         ;;
#     all)
#         patch_login
#         patch_accounts_pool
#         patch_db
#         patch_account
#         ;;
#     *)
#         echo "Invalid option. Use {login|accounts_pool|db|account|all}"
#         ;;
# esac