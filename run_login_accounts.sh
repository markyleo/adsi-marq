#!/bin/bash
echo "Running run_login_accounts.sh on $(date)" > /home/ubuntu/app/adsi-marq/test_cron_log.txt

# Check if the file exists before attempting to delete
if [ -f "/home/ubuntu/app/adsi-marq/accounts.db" ]; then
    echo "File /home/ubuntu/app/adsi-marq/accounts.db exists. Deleting..." >> /home/ubuntu/app/adsi-marq/test_cron_log.txt
    rm /home/ubuntu/app/adsi-marq/accounts.db
    echo "File deleted." >> /home/ubuntu/app/adsi-marq/test_cron_log.txt
else
    echo "File /home/ubuntu/app/adsi-marq/accounts.db does not exist." >> /home/ubuntu/app/adsi-marq/test_cron_log.txt
fi

# Run the Python script
/home/ubuntu/app/adsi-marq/venv/bin/python3 /home/ubuntu/app/adsi-marq/login_accounts.py >> /home/ubuntu/app/adsi-marq/test_cron_log.txt 2>&1