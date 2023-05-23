from flask import *
import pandas as pd
import json
import snscrape.modules.twitter as sntwitter

app = Flask(__name__)

@app.route('/keywords/', methods=['GET'])
def twitter_keyword():
    keyword_qry = str(request.args.get('keywords'))
    threshold = 1
    if int(request.args.get('threshold')) > 1 :
        threshold = int(request.args.get('threshold'))

    print(threshold) 

    scraper = sntwitter.TwitterSearchScraper("'"+keyword_qry+"'")
    tweets = []

    for i, tweet in enumerate(scraper.get_items()):
        data_set = {'id': tweet.id, 'user' : tweet.user.displayname, 'date' : str(tweet.date) ,'content' : str(tweet.rawContent),'username' : tweet.user.username, 'like_count' : tweet.likeCount, 'retweet_count' : tweet.retweetCount}
        if int(tweet.retweetCount) > int(threshold) :
            tweets.append(data_set)
        if i > 300 :
            break

    #tweet_dfs = pd.DataFrame(tweets, columns=["twitter_id","display_name","date","content","username","like_count","retweet_count"])
    #tweet_df = json.dumps(tweets)
    print(str(json.dumps(tweets)))
    return str(json.dumps(tweets))

@app.route('/school/', methods=['GET'])
def school_qry():
    school_qry = str(request.args.get('school_id'))
    
    scraper = sntwitter.TwitterProfileScraper(str(""+school_qry+""))
    tweets = []

    for i, tweet in enumerate(scraper.get_items()):
        data_set = {'id': tweet.id, 'user' : tweet.user.displayname, 'date' : str(tweet.date) ,'content' : tweet.rawContent,'username' : tweet.user.username, 'like_count' : tweet.likeCount, 'retweet_count' : tweet.retweetCount}
        tweets.append(data_set)
        if i > 100 :
            break

    #tweet_dfs = pd.DataFrame(tweets, columns=[,"content","username","like_count","retweet_count"])
    tweet_df = json.dumps(tweets)
    return tweet_df

if __name__ == '__main__' : 
    app.run(port=7777)