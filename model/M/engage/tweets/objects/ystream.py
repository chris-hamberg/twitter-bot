from model.M.engage.tweets.objects.super import SuperTweetObject


class Ystream(SuperTweetObject):


    def __init__(self, admin): super().__init__(admin)


    def execute(self):
        tweet, video = self.preprocessor.get("stream")
        _ = self._subexecution_type1(tweet)
        r = self._subexecution_type2("stream")
        self._terminate(r, video)
        return r, tweet


    def _terminate(self, r, video):
        super()._terminate(r)
        self.admin.orm.api.youtube.update(video[4])
        self.admin.orm.api.state.tweetAI_injection_state = False
