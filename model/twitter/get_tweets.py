import requests
import pickle


class GetTweets:
    def __init__(self):
        self.url = "https://api.twitter.com/2/users/{id}/tweets"

    def request(self, id = None, auth = None, max_results = 5, 
            start_time = None, created_at = False, history = False):
        params = {"max_results": max_results}
        if start_time: params.update({"start_time": start_time})
        if created_at: params.update({"tweet.fields": "created_at"})
        if history:    params.update({
            "expansions" : "author_id,referenced_tweets.id",
            "user.fields": "id,name,username"})
        
        return requests.get(
                self.url.format(id = id),
                params = params,
                auth = pickle.loads(auth))
