# sns-twitter using SNScrape

GET = keywords : string "keyword to be query" { xbox,python }

GET = threshold : int " number of retweets to be fetched" { 2 }

Return value : 

```bash
[ 
    {
        "id": 1660642960344530944, 
        "user": "Xbox Game Pass UK", 
        "date": "2023-05-22 13:45:09+00:00", 
        "content": "\ud83d\udc9a Drop an F in chat with style \ud83d\udc9a\n\nWant to get your fingers on these Custom PC Game Pass keycaps? \ud83d\udc40 \n\nFollow @XboxGamePassUK & RT this tweet for the chance to win \ud83d\udd25 https://t.co/axDg8TUA77", 
        "username": "XboxGamePassUK", 
        "like_count": 25, 
        "retweet_count": 36
   }
]
```
