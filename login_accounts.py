import json
import asyncio
from twscrape import API, gather, AccountsPool
from twscrape.logger import set_log_level
import time
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

if os.path.exists("/home/ubuntu/app/adsi-marq/accounts.db"):
    print("========================= The file accounts.db exists. Deleting... =========================")
    os.remove("/home/ubuntu/app/adsi-marq/accounts.db")
else:
    print("========================= The file accounts.db does not exist =========================")

os.environ["TWS_PROXY"] = "http://IbDxpBQwzg6vkEvu:8fsjGZeNV2YoDtY4@geo.iproyal.com:12321" # randomize per request
# os.environ["TWS_PROXY"] = "http://IbDxpBQwzg6vkEvu:8fsjGZeNV2YoDtY4_session-eGfaqqcM_lifetime-30s@geo.iproyal.com:12321" # sticky IP

api = API()

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
    return None

async def iterate_json(data):
    proper=""
    if isinstance(data, dict):
        for key, value in data.items():
            addition = f"{value}:"
            if key != "csrfCookie" and key != "totpSecret":
                proper += addition     
            if key == "totpSecret":
                addition = f"{value}"
                proper += addition
                await api.pool.add_account(proper.split(":")[0], proper.split(":")[1], proper.split(":")[2], proper.split(":")[3], mfa_code=proper.split(":")[4])
            if isinstance(value, (dict, list)):
                await iterate_json(value)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                await iterate_json(item)

async def main():
    file_path = "/home/ubuntu/app/adsi-marq/accounts.json"
    # delete_file_sync("/Users/francisadish/Desktop/code/adsi-marq/accounts.db")
    # file_path = "/Users/francisadish/Desktop/code/adsi-marq/accounts.json"
    
    json_data = read_json_file(file_path)
    
    if json_data:
        await iterate_json(json_data)

    counter = 0
    while counter < 10:
        print(f"========================= Login all accounts retries: {counter + 1} =========================")
        await api.pool.login_all()
        stats = await api.pool.stats()
        inactive = stats["inactive"]
        if inactive < 1:
            counter = 11
        else:
            time.sleep(15)
            counter += 1
    
    print("========================= Retries executed =========================")
    print(stats)

    send_email_smtp(
        "francis.borlas@adish.com.ph", 
        "francis.borlas.9398@gmail.com", 
        "X Scraper Account Login Logs", 
        "Hi, attached here is the cron job logs for X scraper's account login.",
        file_path="/home/ubuntu/app/adsi-marq/test_cron_log.txt"
    )
    
    del os.environ["TWS_PROXY"]

# def delete_file_sync(file_path):
#     if os.path.exists(file_path):
#         print("========================= The file accounts.db exists. Deleting... =========================")
#         os.remove(file_path)
#     else:
#         print("========================= The file accounts.db does not exist =========================")

def send_email_smtp(sender_email, receiver_email, subject, body, file_path=None):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    if file_path:
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)

            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(file_path)}',
            )

            message.attach(part)
        except Exception as e:
            print(f"Failed to attach the file. Error: {str(e)}")

    try:
        username = os.environ["SMTP_USERNAME"]
        password = os.environ["SMTP_PASSWORD"]
        endpoint = os.environ["SMTP_ENDPOINT"]

        server = smtplib.SMTP(endpoint, 587)
        server.starttls()
        server.login(username, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')
    finally:
        server.quit()

if __name__ == "__main__":
    asyncio.run(main())