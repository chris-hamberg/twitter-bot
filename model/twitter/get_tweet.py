import requests
import pickle


class GetTweet:


    def __init__(self):
        self.url = "https://api.twitter.com/2/tweets/{id}"


    def request(self, id = None, auth = None):
        url = self.url.format(id = id)
        return requests.get(url, auth = pickle.loads(auth))
