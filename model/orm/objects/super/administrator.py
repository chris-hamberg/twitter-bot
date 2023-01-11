from model.objects.exceptions import FollowersWarningException
#from model.objects.exceptions import NoInternetException

from model.orm.api.super.accessor import Accessor
from model.orm.api.state.state import State
from model.orm.api.interface import ORM

from model.objects.exceptions import NullValue
from model.twitter.endpoints import Endpoints

from requests_oauthlib import OAuth1
import pickle
import os



class Twitter:
    def __init__(self, admin): self.api = Endpoints(admin)



class SuperAdministrator:


    def __init__(self, db, id = None, **auth):
        self._db        = db
        self.orm        = ORM(self, db)
        self._accessor  = Accessor(db = db)
        self.twitter    = Twitter(self)
        if id:
            self._id = id; self._read()
            self.orm.api.state = State(self)
        elif auth: self._create(**auth)
        else: raise NullValue("id or authorization required.")
        self.orm.api._init()


    def _create(self, **auth):
        bearer = auth.get("bearer")
        auth   = pickle.dumps(OAuth1(
                auth.get("api_key"),
                auth.get("api_key_secret"),
                auth.get("access_token"),
                auth.get("access_token_secret")))
        r = self.twitter.api(self, None, **{"auth": auth})
        id = r.json().get("data").get("id")
        self._id = id
        self.orm.api.users._create("admin", r, state = False, id = id)
        admin = (id, auth, bearer)
        sql   = (f"INSERT OR IGNORE INTO administrator (id, auth, bearer) "
                  "VALUES (?, ?, ?);")
        self._accessor.execute_commit(sql, admin)

        self._create_files()
        try:
            self.metrics(auth = auth, r = r)
        except FollowersWarningException:
            pass


    def _read(self):
        data = self._getter()
        if not self._id:
            self._id     = data[0]
        self.id          = data[0]
        self.auth        = data[1]
        self.bearer      = data[2]
        self.youtube_api = data[3]
        return self.id, self.auth, self.bearer, self.youtube_api

    
    def _delete(self):
        user = [(self.id, self.name, self.username)]
        self.orm.api.users._delete("admin", user)


    def metrics(self, auth = None, r = None):
        #try:
        if not auth:
            auth = self.auth
        if not r:
            r = self.twitter.api(self, None, **{"auth": auth})
        self.orm.api.state = State(self)
        metrics = r.json().get("data").get("public_metrics")

        followers_count = self.orm.api.state.follower_count
        following_count = self.orm.api.state.following_count

        updated_followers_count = metrics.get("followers_count")
        updated_following_count = metrics.get("following_count")

        if ((following_count == 0) or (followers_count == 0)): pass
        elif (((updated_following_count == 0) and (following_count != 0)) or (
                (updated_followers_count == 0) and (followers_count != 0))):
            raise FollowersWarningException
        elif followers_count >= 1000:
            if ((updated_followers_count / followers_count) <= 0.1):
                raise FollowersWarningException
            if ((updated_following_count / following_count) <= 0.1):
                raise FollowersWarningException

        self.orm.api.state.follower_count  = updated_followers_count
        self.orm.api.state.following_count = updated_following_count
        self.orm.api.state.tweet_count     = metrics.get("tweet_count")
        #except NoInternetException:
        #    pass


    def _create_files(self):
        directory = os.path.join("tweets", f"{self.username}")
        if (not os.path.exists(directory)):
            os.mkdir(directory)
        fnames = ["tweets", "meme_ids", "meme_header", "retweet_keywords",
                  "retweet_blacklist", "reply_text", "username_blacklist",
                  "tweetAI_prompts", "tweetAI_replacements", "ai_knowledge",
                  "ai_instruction", "replyAI_blacklist"]
        for fname in fnames:
            path = os.path.join(directory, fname + ".txt")
            if not os.path.exists(path):
                with open(path, "w") as fhand:
                    pass
