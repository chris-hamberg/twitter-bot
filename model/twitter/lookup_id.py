import requests
import pickle


#NOTE For DMs. DM is not supported by API v2. So this is not used.
class LookupID:
    def __init__(self):
        self.url_stem = "https://api.twitter.com/2/users/"
        self.params   = {"user.fields": "description"}

    def request(self, id = None, auth = None): 
        url = self.url_stem + str(id)
        return requests.get(
                url,
                params = self.params,
                auth   = pickle.loads(auth))
