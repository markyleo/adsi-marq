# M.A.R.Q ( Multiple API Retrieval Query )

Can fetch on Twitter/Facebook/Instagram

GET = query : string "keyword to be query" { xbox,python }

GET = threshold : int " number of retweets to be fetched" { 2 }

Return value : 

```bash
[ 
    {
        "id": 1660642960344530944, 
        "user": "Xbox Game Pass UK", 
        "date": "2023-05-22 13:45:09+00:00", 
        "content": "Guys Please Check this thread related to Power Transformer in #machinelearning ✨
           #100DaysOfCode #programming
           #DataScience #dataScientist #analysts #SQL #Python", 
        "username": "XboxGamePassUK", 
        "like_count": 25, 
        "retweet_count": 36
   }
]
```

## Setup  
```
python3.10 -m venv venv  
source venv/bin/activate  
pip3 install -r requirements.txt
sh patch.sh accounts_pool  
```

## X Accounts Login Steps
1. Create `accounts.json` file on project root. You can see the data format in the existing `accounts.json` file.  
2. Run `python3 login_accounts.py`  
3. Run `twscrape accounts` or `twscrape stats` to check accounts status  
4. Run `twscrape search "elon mask lang:es" --limit=5` to check if the scraper can fetch data  

## Operation Notes
* Logging in accounts uses Proxy Service to bypass IP Ban error. Not using Proxy will lessen the probability of successful login. I availed the proxy from [IPRoyal](https://iproyal.com). You can use any Proxy Providers you prefer.  
* You can acquire accounts for a minimal cost from [Twaccs](https://twaccs.com).
* Note that it would be better to have surplus of accounts from Twaccs since they sometimes run out of stock.  
* Login script will run via crontab every 7am, 11am, 3pm, 7pm, 11pm, 3am.
* Script execution logs will be emailed to whomever is set inside the `login_accounts.py` line 78.

