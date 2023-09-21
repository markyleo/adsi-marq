from flask import *
from datetime import date
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from contextlib import aclosing



app = Flask(__name__)

@app.route('/')
def hello_scrape():
    return 'Twitter-Scraper'

@app.route('/keywords/', methods=['GET'], strict_slashes=False)
def twitter_keyword():
    keyword_qry = str(request.args.get('query'))
    threshold = 1
    today = str(date.today())
    if int(request.args.get('threshold')) >= threshold :
        threshold = int(request.args.get('threshold'))

    print(threshold) 
    tweets = []
    scraper = str("'"+keyword_qry+" min_retweets:"+str(threshold)+" since:"+today+"'")

    async def exec(scraper,threshold):
        api = API()
        await api.pool.add_account("FBorlas27326", "P@ssw0rd123_d3l!ght", "_", "_", cookies='_ga=GA1.2.1609834860.1694653401; lang=en; g_state={"i_l":0}; _gid=GA1.2.183376484.1695188529; kdt=5QFcOHpAxf1SCwfxLy6k0JQUwKG85g6LPUPypaBr; dnt=1; guest_id=v1%3A169525928510254887; guest_id_marketing=v1%3A169525928510254887; guest_id_ads=v1%3A169525928510254887; gt=1704667112244175097; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCKzsU7WKAToMY3NyZl9p%250AZCIlZDY4ZDQ3OGE3OWU4OTgzY2VmNGQ2Njc3NWM2ZmEyMzU6B2lkIiUwZTRi%250AOWRjN2E1Nzk5ODI4MDUzZTYwMjBhNGNkMThkNA%253D%253D--ecc8edb0d4263e9c36db2f3340225b247b2a2bb9; auth_token=77c0eb33fc09fc0b5f6c1e7d6b8d98efe762e0a1; ct0=d20118e356ffa2621c26f2c6c893ff5594285f6c6048609f8c62c15c47a9523bdabf9dc2cc5a601441aa08a5326355bb3a6719f85071c9b1a7d66d5686e0f5f8855d31ceb77c7271bd028fe6bffb59fc; twid=u%3D1702125927969505280; att=1-k16v7P8pSbXgxNkcvcw1fggRgi1bLb4tf8mDDbd2; personalization_id="v1_ELmc+y72Iu+rbXoooHKrWw=="')
        await api.pool.add_account("AdsiBanana","ADSIB@n@n@31118","-","-")
        await api.pool.add_account("dev_pazu_test","Secured@1230","-","-")
        await api.pool.login_all()
        tweet_count = 0

        async with aclosing(api.search(scraper, limit=10)) as gen:
            async for tweet in gen:
                tweet_count+=1
                data_set = {'id': tweet.id, 'user' : tweet.user.displayname, 'date' : tweet.date ,'content' : tweet.rawContent,'url' : tweet.url,'media' : tweet.media,'username' : tweet.user.username, 'like_count' : tweet.likeCount, 'retweet_count' : tweet.retweetCount}
                tweets.append(data_set)
                if tweet_count > 9 :
                    break
        
    asyncio.run(exec(scraper,threshold))

    print(jsonify(tweets))
    return jsonify(tweets)


if __name__ == '__main__' : 
    app.run()
