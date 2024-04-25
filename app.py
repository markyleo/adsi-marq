from flask import *
#import pandas as pd
#import json
from datetime import date
from twscrape import API
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import twitter as sntwitter
import os 

app = Flask(__name__)

@app.route('/')
async def hello_scrape():
    # api = API()

    # stats = await api.pool.stats()
    # accounts = await api.pool.get_all()

    # print(accounts)

    return 'SNS-Twitter-Scrape'

@app.route('/keywords/', methods=['GET'], strict_slashes=False)
async def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    today = str(date.today())
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    print(threshold) 

    try:
        scraper = sntwitter.TwitterSearchScraper("'"+keyword_qry+" since:"+today+"'")
        tweets = []

        for i, tweet in enumerate(scraper.get_items()):
            data_set = {'id': tweet.id, 'user' : tweet.user.displayname, 'date' : tweet.date ,'content' : tweet.rawContent,'url' : tweet.url,'media' : tweet.media,'username' : tweet.user.username, 'like_count' : tweet.likeCount, 'retweet_count' : tweet.retweetCount}
            if int(tweet.retweetCount) >= int(threshold) :
                tweets.append(data_set)
            if i > 200 :
                break
                
        print(jsonify(tweets))
        return jsonify(tweets)
    except Exception as e:
        api = API()

        stats = await api.pool.stats()
        accounts = await api.pool.accounts_info()

        thisdict = {
            "accounts": accounts,
            "stats": stats,
            "error": str(e)
        }

        send_email_smtp('francis.borlas@adish.com.ph', 'francis.borlas.9398@gmail.com', 'Scraper Error', str(thisdict))

        print(accounts)
        print(e)
        return jsonify(thisdict)


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

if __name__ == '__main__' : 
    app.run()
