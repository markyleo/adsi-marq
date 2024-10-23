from flask import *
from datetime import date
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from contextlib import aclosing
from asgiref.wsgi import WsgiToAsgi
from twitter_search_validator import TwitterSearchValidator
import json

api = API()
app = Flask(__name__)

@app.route('/')
def hello_scrape():
    return 'MARQ adsi twitter-scraper'

@app.route('/keywords/', methods=['GET'], strict_slashes=False)
async def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    today = str(date.today())
    # today = str(date(2024, 8, 2))
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    tweets = []
    scraper = f'{keyword_qry} min_retweets:{threshold} lang:ja since:{today}'
    # scraper = f'{keyword_qry} min_retweets:{threshold} lang:ja'

    async def exec(scraper):
        tweet_count = 0

        async with aclosing(api.search(scraper, limit=5)) as gen:
            async for tweet in gen:
                tweet_count += 1
                data_set = {
                    'id': tweet.id,
                    'user': tweet.user.displayname,
                    'date': tweet.date,
                    'content': tweet.rawContent,
                    'url': tweet.url,
                    'media': tweet.media,
                    'username': tweet.user.username,
                    'like_count': tweet.likeCount,
                    'retweet_count': tweet.retweetCount,
                    'inReplyToUsername': getattr(tweet.inReplyToUser, 'username', None),
                    'mentions': [user.username for user in tweet.mentionedUsers]
                }
                tweets.append(data_set)
                if tweet_count > 4:
                    break

    await exec(scraper)

    validator = TwitterSearchValidator(keyword_qry)

    valid_posts = []

    for post in tweets:
        is_valid = validator.validate_post(post)
        
        if is_valid:
            valid_posts.append(post)

    return jsonify(valid_posts)

@app.route('/search/', methods=['GET'], strict_slashes=False)
async def twitter_search():
    keyword_qry = int(request.args.get('query'))
    threshold = 1
    today = str(date.today())
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    tweet = []

    async def exec():
        tweet.append(await api.tweet_details(keyword_qry))
    
    await exec()

    return jsonify(tweet)

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(port=8000)