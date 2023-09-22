from flask import *
from datetime import date
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from contextlib import aclosing
import json

api = API()

async def init_login():
    file_path = "//wsl.localhost/Ubuntu/home/markyy/app/adsi-marq/accounts.json"

    with open(file_path, 'r') as json_file:
        accounts_data = json.load(json_file)

    for item in accounts_data:
        await api.pool.add_account(item["username"], item["password"], "_", "_")

    await api.pool.login_all()

app = Flask(__name__)

@app.route('/')
def hello_scrape():
    return 'MARQ adsi twitter-scraper'

@app.route('/keywords/', methods=['GET'], strict_slashes=False)
def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    today = str(date.today())
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    tweets = []
    scraper = str("'"+keyword_qry+" min_retweets:"+str(threshold)+" since:"+today+"'")

    async def exec(scraper):
        tweet_count = 0

        async with aclosing(api.search(scraper, limit=10)) as gen:
            async for tweet in gen:
                tweet_count+=1
                data_set = {'id': tweet.id, 'user' : tweet.user.displayname, 'date' : tweet.date ,'content' : tweet.rawContent,'url' : tweet.url,'media' : tweet.media,'username' : tweet.user.username, 'like_count' : tweet.likeCount, 'retweet_count' : tweet.retweetCount}
                tweets.append(data_set)
                if tweet_count > 9 :
                    break
        
    asyncio.run(exec(scraper))

    return jsonify(tweets)


if __name__ == '__main__' : 
    app.run(asyncio.run(init_login()))
