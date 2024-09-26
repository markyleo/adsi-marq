#!/bin/bash
# Delete the file first
if [ -f "/home/ubuntu/app/adsi-marq/accounts.db" ]; then
    echo "Deleting /home/ubuntu/app/adsi-marq/accounts.db..."
    rm /home/ubuntu/app/adsi-marq/accounts.db
fi

# Run the Python script
/home/ubuntu/app/adsi-marq/venv/bin/python3 /home/ubuntu/app/adsi-marq/login_accounts.py > /home/ubuntu/app/logs/login_accounts.log 2>&1