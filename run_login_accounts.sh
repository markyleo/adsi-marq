#!/bin/bash
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

echo "Running run_login_accounts.sh on $(date)"

# Check if the file exists before attempting to delete
if [ -f "/home/ubuntu/app/adsi-marq/accounts.db" ]; then
    echo "File /home/ubuntu/app/adsi-marq/accounts.db exists. Deleting..."
    rm /home/ubuntu/app/adsi-marq/accounts.db
    echo "File deleted."
else
    echo "File /home/ubuntu/app/adsi-marq/accounts.db does not exist."
fi

# Run the Python script
/home/ubuntu/app/adsi-marq/venv/bin/python3 /home/ubuntu/app/adsi-marq/login_accounts.py