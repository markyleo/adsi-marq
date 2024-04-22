import boto3
from botocore.exceptions import ClientErrorfrom 
from flask import *
#import pandas as pd
#import json
from datetime import date
import snscrape.modules.twitter as sntwitter



app = Flask(__name__)

@app.route('/')
def hello_scrape():
    send_email('Test Subject', 'Test Body', 'francis.borlas@adish.com.ph', 'francis.borlas.9398@gmail.com')
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

def send_email(subject, body_text, sender, recipient):
    # Create a new SES client
    ses_client = boto3.client('ses')

    # Try to send the email
    try:
        # Provide the contents of the email
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender,
        )
    # Handle errors
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:", response['MessageId'])


if __name__ == '__main__' : 
    app.run()
