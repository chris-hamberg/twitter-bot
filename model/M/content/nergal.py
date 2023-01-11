from model.M.engage.compositors.filter_compositor import FilterCompositor
from datetime import timedelta
from datetime import datetime
import logging
import random
import time


log = logging.getLogger(__name__)


ζ, α, β, CCL, D, M = 0, 1, 2, 250, 500, 1000


class Nergal:


    def __init__(self, admin):
        self.filter   = FilterCompositor(admin)
        self.admin    = admin
        self.name     = "destroyer"
        self._methods = [
                self._clean_unfriendQ, 
                self._delete_tweets,
                self._delete_users, 
                self._delete_orphans,
                self._delete_redundant_tweetAI_tweets,
                self._delete_filter_tweets]


    def execute(self):
        try:
            index = self.admin.orm.api.state.destroyer_index
            self._methods[index]()
            time.sleep(2)
        except IndexError:
            self.admin.orm.api.state.destroyer_index = index = 0
            self._methods[index]()
            time.sleep(2)
        finally:
            self.admin.orm.api.state.destroyer_index = index + 1
            self._close()


    def _delete_redundant_tweetAI_tweets(self):
        tweets = self.admin.orm.api.tweets.read(type='tweetAI', replied=False)
        for e, t1 in enumerate(tweets):
            for t2 in tweets[e + 1:]:
                if (t1[1] == t2[1]): self.admin.orm.api.tweets.delete(t2[0])
        tweets2 = self.admin.orm.api.tweets.count(type='tweetAI', replied=False)
        destroyed = len(tweets) - tweets2
        if destroyed:
            message = f"Destroyed {destroyed} redundant tweets from queue."
        else: message = "Finished searching for redundant tweet content."
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")


    def _delete_filter_tweets(self):
        self.filter.refresh_blacklist(); self.filter.refresh_keywords()
        self.filter.refresh_blacklisted_users()
        params = {"type": "reply_type1", "replied": False}
        tweets = self.admin.orm.api.tweets.read(**params)
        params.update({"type": "reply_type2"})
        tweets.extend(self.admin.orm.api.tweets.read(**params))
        ι, δ = self.admin.orm.api.state.tfilter_index, ζ
        if (len(tweets) <= ι): self.admin.orm.api.state.tfilter_index = ι = ζ
        for tweet in tweets[ι:ι + D]:
            tweet_id, text, uid = tweet[ζ], tweet[α], tweet[β]
            if not text: continue
            try: user = self.admin.orm.api.tweets.user(uid)[ζ][β]
            except IndexError: user = None
            Π = self.filter.filter(text, user = user)
            if Π: self.admin.orm.api.tweets.delete(tweet_id); δ += α
            time.sleep(0.03)
        self.admin.orm.api.state.tfilter_index = ι + D
        if δ: message = f"Destroyed {δ} tweets via filtration."
        else: message = f"Finished filtration on tweets."
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")


    def _delete_tweets(self):
        delta, e = datetime.utcnow() - timedelta(weeks = 12), 0
        tweets   = self.admin.orm.api.tweets.read(delta = delta)
        for e, tweet in enumerate(tweets):
            tweet_id = tweet[0]
            self.admin.orm.api.tweets.delete(tweet_id)
        if e: 
            e += 1
            message = f"Destroyed {e} tweets that were more than 4 weeks old."
        else: message = "Finished check for expired data."
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")
        

    def _delete_users(self):
        delta = datetime.utcnow() - timedelta(weeks = 52)
        blacklist = self.admin.orm.api.users.read('blacklist', delta = delta)
        self.admin.orm.api.users.delete('blacklist', blacklist)
        e = len(blacklist)
        if e:
            msg = f"Destroyed {e} users that were blacklisted for over a year."
        else: msg = "Finished check for blacklist release."
        self.admin.orm.api.messages.create(msg, self.name)
        log.debug(f"{self.admin.name}\n{msg}")


    def _clean_unfriendQ(self):
        following = self.admin.orm.api.users.read("following", short = True)
        unfriend  = self.admin.orm.api.users.read("unfriendQ", short = True)
        badQ = [user for user in unfriend if user not in following]
        self.admin.orm.api.users.delete("unfriendQ", badQ)
        self.admin.orm.api.state.unfriendQ_count = (
                self.admin.orm.api.users.count("unfriendQ"))
        message = f"Sanity check on \u03C7Q completed."
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")


    def _delete_orphans(self):
        ids = self.admin.orm.api.users.orphans()
        if ids: message = f"Destroyed {len(ids)} orphans."
        else:   message = "Finished searching for orphans."
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")


    def _close(self):
        n = random.randint(5, 15)
        delta = datetime.utcnow() + timedelta(minutes = n)
        self.admin.orm.api.state.destroyer_delta = delta
