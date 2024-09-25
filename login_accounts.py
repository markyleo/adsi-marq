import json
import asyncio
from twscrape import API, gather, AccountsPool
from twscrape.logger import set_log_level
import time
import requests
import os

os.environ["TWS_PROXY"] = "http://IbDxpBQwzg6vkEvu:8fsjGZeNV2YoDtY4@geo.iproyal.com:12321" # randomize per request
# os.environ["TWS_PROXY"] = "http://IbDxpBQwzg6vkEvu:8fsjGZeNV2YoDtY4_session-eGfaqqcM_lifetime-30s@geo.iproyal.com:12321" # sticky IP

os.environ["SMTP_USERNAME"] = "AKIASNNFRYSNJDMCIF5W"
os.environ["SMTP_PASSWORD"] = "BGwhDgbH8Xx11HpqfxDwitmge10cVutt0Ply0BWvUlwG"
os.environ["SMTP_ENDPOINT"] = "email-smtp.ap-northeast-1.amazonaws.com"

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

async def iterate_json(data, api):
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
                print(proper)
            if isinstance(value, (dict, list)):
                await iterate_json(value, api)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                await iterate_json(item, api)

async def main():
    file_path = '/home/ubuntu/app/adsi-marq/accounts.json'  # Replace with the path to your JSON file
    json_data = read_json_file(file_path)
    
    api = API()

    if json_data:
        await iterate_json(json_data, api)

    counter = 0
    while counter < 10:
        print(f"========================= Login all accounts retries: {counter + 1} =========================")
        # await api.pool.login_all()
        stats = await api.pool.stats()
        inactive = stats["inactive"]
        if inactive < 1:
            counter = 11
        else:
            time.sleep(30)
            counter += 1
    
    print("========================= Retries executed =========================")
    print(stats)
    send_email_smtp("francis.borlas@adish.com.ph", "francis.borlas.9398@gmail.com", "Twitter Scraper Account Login Logs", "The bodyyy")
    del os.environ["TWS_PROXY"]

def send_email_smtp(sender_email, receiver_email, subject, body):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Create SMTP session for sending the mail
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
        server.quit()  # Quit the SMTP session

if __name__ == "__main__":
    asyncio.run(main())