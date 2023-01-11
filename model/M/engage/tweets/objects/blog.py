from model.M.engage.tweets.objects.super import SuperTweetObject


class Blog(SuperTweetObject):


    def __init__(self, admin): super().__init__(admin)


    def execute(self):
        tweet, url, protocol = self.preprocessor.get("blog")
        _ = self._subexecution_type1(tweet)
        r = self._subexecution_type2("blog")
        self._terminate(r, url, protocol)
        return r, tweet


    def _terminate(self, r, url, protocol):
        super()._terminate(r)
        url = f"{protocol}://{url}"
        self.admin.orm.api.blog.update(url)
        self.admin.orm.api.state.tweetAI_injection_state = False
