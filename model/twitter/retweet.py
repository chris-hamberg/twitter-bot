import requests
import pickle
import json


class Retweet:


    def __init__(self):
        self.url = "https://api.twitter.com/2/users/{id}/retweets"


    def request(self, id = None, tweet_id = None, auth = None):
        return requests.post(
                url = self.url.format(id = id),
                headers = {"Content-Type": "application/json"},
                data = json.dumps({"tweet_id": str(tweet_id)}),
                auth = pickle.loads(auth))
