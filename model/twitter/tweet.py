import requests
import pickle
import json


class Tweet:

    def __init__(self):
        self.url = "https://api.twitter.com/2/tweets"

    def request(self, tweet = None, token = None, auth = None, media = None, 
            tweet_id = None):
        data = {"text": tweet}
        if media:
            data.update({"media": {"media_ids": [str(media)]}})
        elif tweet_id:
            data.update({"reply": {"in_reply_to_tweet_id": str(tweet_id)}})
        return requests.post(
                self.url,
                data    = json.dumps(data),
                headers = {"Content-Type" : "application/json",
                           "Authorization": f"Bearer {token}"},
                auth    = pickle.loads(auth))
