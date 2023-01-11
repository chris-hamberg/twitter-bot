import requests
import pickle


class Followers:
    def __init__(self):
        self.url = "https://api.twitter.com/2/users/{id}/followers"

    def request(self, id = None, page = None, auth = None):
        return requests.get(
                self.url.format(id = id), 
                params = {"pagination_token": page, 
                          "max_results": 1000},
                auth = pickle.loads(auth))


class Scraper(Followers): pass
