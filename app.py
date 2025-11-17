from flask import *
from datetime import date
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from contextlib import aclosing
from asgiref.wsgi import WsgiToAsgi
from twitter_search_validator import TwitterSearchValidator
import json
from datetime import date, timedelta
import re

api = API()
app = Flask(__name__)

@app.route('/')
def hello_scrape():
    return 'MARQ adsi twitter-scraper'

# @app.route('/keywords/', methods=['GET'], strict_slashes=False)
# def twitter_keyword():
#     data = [
#         {
#             "content": " Testing Duplicate Content",
#             "date": "Thu, 23 Jan 2025 14:49:29 GMT",
#             "id": 1876279930482557418,
#             "inReplyToUsername": None,
#             "like_count": 341,
#             "media": {
#                 "animated": [
#                     {
#                         "thumbnailUrl": "https://pbs.twimg.com/tweet_video_thumb/GgniplRbEAAT5rf.jpg",
#                         "videoUrl": "https://video.twimg.com/tweet_video/GgniplRbEAAT5rf.mp4"
#                     }
#                 ],
#                 "photos": [],
#                 "videos": []
#             },
#             "mentions": [],
#             "retweet_count": 37,
#             "url": "https://x.com/BitcoinTech5/status/1876279930482557418",
#             "user": "Foxx🦊ビットコイン投資家",
#             "username": "TESTDUPUSER2"
#         },
#         {
#             "content": " Testing Duplicate Content",
#             "date": "Thu, 23 Jan 2025 14:49:29 GMT",
#             "id": 1876279930482557419,
#             "inReplyToUsername": None,
#             "like_count": 341,
#             "media": {
#                 "animated": [
#                     {
#                         "thumbnailUrl": "https://pbs.twimg.com/tweet_video_thumb/GgniplRbEAAT5rf.jpg",
#                         "videoUrl": "https://video.twimg.com/tweet_video/GgniplRbEAAT5rf.mp4"
#                     }
#                 ],
#                 "photos": [],
#                 "videos": []
#             },
#             "mentions": [],
#             "retweet_count": 37,
#             "url": "https://x.com/BitcoinTech5/status/1876279930482557418",
#             "user": "Foxx🦊ビットコイン投資家",
#             "username": "TESTDUPUSER1"
#         },
#         {
#             "content": " Testing Duplicate Content",
#             "date": "Thu, 23 Jan 2025 14:49:29 GMT",
#             "id": 1876279930482557420,
#             "inReplyToUsername": None,
#             "like_count": 341,
#             "media": {
#                 "animated": [
#                     {
#                         "thumbnailUrl": "https://pbs.twimg.com/tweet_video_thumb/GgniplRbEAAT5rf.jpg",
#                         "videoUrl": "https://video.twimg.com/tweet_video/GgniplRbEAAT5rf.mp4"
#                     }
#                 ],
#                 "photos": [],
#                 "videos": []
#             },
#             "mentions": [],
#             "retweet_count": 37,
#             "url": "https://x.com/BitcoinTech5/status/1876279930482557418",
#             "user": "Foxx🦊ビットコイン投資家",
#             "username": "TESTDUPUSER"
#         }
#     ]
#     return jsonify(data)

@app.route('/keywords/', methods=['GET'], strict_slashes=False)
async def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    today = str(date.today() - timedelta(days=7))
    # today = str(date(2024, 8, 2))
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    sanitized_keyword = clean_or_query(keyword_qry)
    print(sanitized_keyword)

    tweets = []
    scraper = f'{sanitized_keyword} min_retweets:{threshold} lang:ja since:{today}'
    # scraper = f'{keyword_qry} min_retweets:{threshold} lang:ja'

    async def exec(scraper):
        tweet_count = 0

        async with aclosing(api.search(scraper, limit=20)) as gen:
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
                if tweet_count > 19:
                    break

    await exec(scraper)

    validator = TwitterSearchValidator(sanitized_keyword)

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

def clean_or_query(input_string):
    def remove_quotes_in_group(match):
        # match.group(1) contains the inside of the parenthesis
        terms = match.group(1).split('OR')
        cleaned_terms = [term.strip().strip('"') for term in terms]
        return '(' + ' OR '.join(cleaned_terms) + ')'

    # Replace all (...) groups one by one
    return re.sub(r'\(([^()]+)\)', remove_quotes_in_group, input_string)

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(port=8000)