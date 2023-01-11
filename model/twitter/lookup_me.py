import requests
import pickle


class LookupMe:
    def __init__(self):
        self.url = "https://api.twitter.com/2/users/me"

    def request(self, auth = None):
        return requests.get(
                self.url, 
                params = {"user.fields": "public_metrics"},
                auth = pickle.loads(auth))
