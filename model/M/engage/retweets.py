from model.M.super.superclass import SuperManager
from model.objects.exceptions import ForbiddenException
from model.objects.exceptions import ProtectedException
import traceback
import random
import time


class RetweetManager(SuperManager):

    
    def __init__(self, admin):
        super().__init__()
        self.params = {"id":admin.id, "auth":admin.auth, "tweet_id":None}
        self.name  = "retweets"
        self.admin = admin


    def retweet(self, tweet, name = None):
        id, text, t = tweet[0], tweet[1], random.randint(1, 3)
        self.params.update({"tweet_id": str(id)})
        try: r = self._handler(**self.params)
        except ForbiddenException as HTTP_403: raise ForbiddenException
        except ProtectedException as HTTP_400:
            e = traceback.format_exc(); self.report(e, name)
        else:
            count = self.admin.orm.api.state.tweet_count + 1
            self.admin.orm.api.state.tweet_count = count
            self.report(f"Retweeted {int(id)}.", name)
            return r
        finally: time.sleep(t)
