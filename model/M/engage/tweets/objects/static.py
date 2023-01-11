from model.M.engage.tweets.objects.super import SuperTweetObject


class Static(SuperTweetObject):


    def __init__(self, admin): super().__init__(admin)


    def execute(self):
        tweet = self.preprocessor.get("static")
        _ = self._subexecution_type1(tweet)
        r = self._subexecution_type2("static")
        self._terminate(r)
        return r, tweet


    def _terminate(self, r):
        super()._terminate(r)
        index = self.admin.orm.api.state.tweetHardcoded_index
        self.admin.orm.api.state.tweetHardcoded_index = index + 1
        self.admin.orm.api.state.tweetAI_injection_state = False
