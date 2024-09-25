import datetime

# Define the log file path
log_file = "/home/ubuntu/app/adsi-marq/test_cron_log.txt"

# Get the current date and time
now = datetime.datetime.now()

# Write the date and time to the log file
with open(log_file, "a") as file:
    file.write(f"Cron job ran at: {now}\n")