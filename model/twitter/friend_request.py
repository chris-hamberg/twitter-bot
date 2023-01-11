import requests
import pickle
import json


class FriendRequest:
    def __init__(self):
        self.url = "https://api.twitter.com/2/users/{admin_id}/following"

    def request(self, admin_id = None, id = None, token = None, auth = None):
        return requests.post(
                self.url.format(admin_id = admin_id), 
                headers = {"Authorization": f"Bearer {token}",
                           "Content-Type": "application/json"}, 
                data = json.dumps({"target_user_id": str(id)}), 
                auth = pickle.loads(auth))
