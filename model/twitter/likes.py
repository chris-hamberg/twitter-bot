import requests
import pickle
import json


class Like:

    def __init__(self):
        self.url = "https://api.twitter.com/2/users/{admin_id}/likes"

    def request(self, admin_id = None, tweet_id = None, auth = None):
        return requests.post(
                self.url.format(admin_id = admin_id), 
                headers = {"Content-Type": "application/json"}, 
                data = json.dumps({"tweet_id": str(tweet_id)}),
                auth = pickle.loads(auth))
            
