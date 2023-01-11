import requests
import pickle


class FriendDelete:
    def __init__(self):
        self.url = ("https://api.twitter.com/2/users/{admin_id}/"
                    "following/{id}")

    def request(self, admin_id = None, id = None, token = None, auth = None): 
        return requests.delete(
                self.url.format(admin_id = admin_id, id = id), 
                headers = {"Authorization": f"Bearer {token}",
                           "Content-Type": "application/json"},
                auth = pickle.loads(auth))
