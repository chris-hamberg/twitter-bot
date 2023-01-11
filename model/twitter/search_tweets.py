import requests
import pickle


class SearchTweets:
    def __init__(self):
        self.url = "https://api.twitter.com/2/tweets/search/recent"

    def request(self, query = None, page = None, auth = None, since_id = None,
            history = None):

        params = {"query": query, "pagination_token": page, "max_results": 100,
                  "expansions": "author_id", "user.fields": "id,name,username"}
        if since_id: params.update({"since_id": since_id})
        if history: params.update({"expansions": 
            "author_id,referenced_tweets.id"})

        return requests.get(
                self.url,
                params = params,
                auth = pickle.loads(auth))
