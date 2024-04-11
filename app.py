import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import *
#import pandas as pd
#import json
from datetime import date
import snscrape.modules.twitter as sntwitter

app = Flask(__name__)

@app.route('/')
def hello_scrape():
    return 'SNS-Twitter-Scrape'

@app.route('/keywords/', methods=['GET'], strict_slashes=False)
def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    today = str(date.today())
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    print(threshold) 

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

def send_email(sender_email, receiver_email, subject, message)
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()  # Secure the connection
        # Login to your account
        server.login('your_email@example.com', 'your_password')
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == '__main__' : 
    app.run()
