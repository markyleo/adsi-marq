from flask import *
import pandas as pd
import json
import snscrape.modules.twitter as sntwitter

app = Flask(__name__)

@app.route('/')
def hello_scrape():
    return 'SNS-Twitter-Scrape'

@app.route('/keywords/', methods=['GET'])
def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    if int(request.args.get('threshold')) > 1 :
        threshold = int(request.args.get('threshold'))

    print(threshold) 

    scraper = sntwitter.TwitterSearchScraper("'"+keyword_qry+"'")
    tweets = []

    for i, tweet in enumerate(scraper.get_items()):
        data_set = {'id': tweet.id, 'user' : tweet.user.displayname, 'date' : str(tweet.date) ,'content' : str(tweet.rawContent),'media' : str(tweet.media,'username') : tweet.user.username, 'like_count' : tweet.likeCount, 'retweet_count' : tweet.retweetCount}
        if int(tweet.retweetCount) > int(threshold) :
            tweets.append(data_set)
        if i > 100 :
            break
            
    print(str(json.dumps(tweets)))
    return str(json.dumps(tweets))


if __name__ == '__main__' : 
    app.run()
