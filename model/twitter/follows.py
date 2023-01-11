import requests
import pickle


class Follows:
    def __init__(self):
        self.url = "https://api.twitter.com/2/users/{id}/following"

    def request(self, id = None, page = None, auth = None):
        return requests.get(
                self.url.format(id = id),
                params = {"pagination_token": page,
                          "max_results": 1000},
                auth = pickle.loads(auth))
