from model.M.parser.dialog import Dialog


class TweetParser:


    def __init__(self, admin):
        self.admin         = admin
        self.conversations = []


    def parse(self, r, type = None, query = None):
        self.conversations.clear()
        self.type, self.query = type, query
        if not r.json().get("data"): return []
        for tweet in r.json().get("data"):
            tweet_id, text, author_id = self._sigma(tweet)
            if ("RT" in text): continue
            self.conversations.append(Dialog())
            self._set_username(r, author_id)
            convo_id = self._get_convo_id(r, tweet)
            self.conversations[-1].id = convo_id
            self._construct(tweet, convo_id)
            self._sentinel_type1()
        return self.conversations


    def _sentinel_type1(self):
        convo = self.conversations[-1]
        for conversation in self.conversations[:-1]:
            if (convo.id == conversation.id):
                self.conversations.pop(-1)
                break


    def _sentinel_type2(self, referenced_tweets):
        if not referenced_tweets: return None
        else: return referenced_tweets[0]


    def _sentinel_type3(self, referenced_tweets):
        if (not referenced_tweets):      return True
        type = referenced_tweets.get("type")
        if (not (type == "replied_to")): return True


    def _preprocess_type1(self, tweet):
        convo_id          = tweet.get("id")
        referenced_tweets = tweet.get("referenced_tweets")
        referenced_tweets = self._sentinel_type2(referenced_tweets)
        return convo_id, referenced_tweets


    def _preprocess_type2(self, r, referenced_tweets):
        reference_id    = referenced_tweets.get("id")
        included_tweets = r.json().get("includes").get("tweets") or []
        return reference_id, included_tweets


    def _sigma(self, tweet):
        tweet_id  = tweet.get("id")
        text      = tweet.get("text")
        author_id = tweet.get("author_id")
        return tweet_id, text, author_id


    def _set_username(self, r, author_id):
        if not r.json().get("includes"): 
            self.conversations[-1].username = None; return False
        users     = r.json().get("includes").get("users")
        try: user = list(filter(lambda u: u.get("id") == author_id, users))[0]
        except IndexError: username = None
        else: username = user.get("username")
        self.conversations[-1].username = username


    def _get_convo_id(self, r, tweet):
        convo_id, ref_tweets = self._preprocess_type1(tweet)
        if self._sentinel_type3(ref_tweets): return convo_id
        ref_id,   inc_tweets = self._preprocess_type2(r, ref_tweets)
        prev_tweet           = self._match(ref_id, inc_tweets)
        params = {"tweet": tweet, "rid": ref_id, "cid": convo_id}
        params.update({"ptweet": prev_tweet})
        if prev_tweet: convo_id = self._eval(**params)
        self.conversations[-1].id = convo_id
        return convo_id


    def _eval(self, tweet, rid, cid, ptweet):
        cid = self._search_database(rid, cid)
        if (cid == tweet.get("id")): return self._begin_convo(ptweet)
        else: return cid


    def _begin_convo(self, prev_tweet):
        convo_id = prev_tweet.get("id")
        self._construct(prev_tweet, convo_id, type = "history")
        return convo_id


    def _construct(self, tweet, convo_id, type = None):
        if   ((type) and bool(self.query) and (isinstance(self.query, str))):
            gamma = (self.admin.id, type, self.query)
        elif ((type) and bool(self.query)):
            gamma = (self.admin.id, type, self.query.q)
        elif (bool(self.query) and (isinstance(self.query, str))):
            gamma = (self.admin.id, self.type, self.query)
        elif  bool(self.query): 
            gamma = (self.admin.id, self.query.type, self.query.q)
        else:          
            gamma = (self.admin.id, self.type, self.query)
        tweet = self._sigma(tweet) + gamma + (convo_id,)
        self.conversations[-1].dialog = tweet


    def _match(self, ref_id, included_tweets):
        for tweet in included_tweets:
            tweet_id = tweet.get("id")
            if (ref_id == tweet_id): return tweet
        return None


    def _search_database(self, reference_id, convo_id):
        ref = self.admin.orm.api.tweets.read(tweet_id = reference_id)
        if ref: return ref[0][9]
        else:   return convo_id
