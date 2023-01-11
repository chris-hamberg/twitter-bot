import requests
import pickle


class LookupUsername:
    def __init__(self):
        self.url = "https://api.twitter.com/2/users/by/username/{username}"

    def request(self, username = None, auth = None): 
        return requests.get(
                self.url.format(username = username), 
                auth = pickle.loads(auth))
