from model.M.engage.tweets.objects.super import SuperTweetObject
import os


class Meme(SuperTweetObject):


    def __init__(self, admin): super().__init__(admin)


    def execute(self):
        tweet, media = self.preprocessor.get("meme")
        self.params.update({"media": media})
        _ = self._subexecution_type1(tweet)
        r = self._subexecution_type2("meme", media)
        self._terminate(r, media)
        return r, tweet


    def _terminate(self, r, media):
        super()._terminate(r)
        index = self.admin.orm.api.state.tweetMeme_index
        self.admin.orm.api.state.tweetMeme_index = index + 1
        if (r.status_code == 400): self._destroy(media)
        self.admin.orm.api.state.tweetAI_injection_state = False


    def _destroy(self, media):
        path = os.path.join("tweets", f"{self.admin.username}", "meme_ids.txt")
        with open(path, "r") as fhand: ids = fhand.read()
        ids = ids.split("\n")
        index = ids.index(str(media))
        ids.pop(index)
        ids = "\n".join(ids)
        with open(path, "w") as fhand: fhand.write(ids)
        index = self.admin.orm.api.state.tweetMeme_index
        self.admin.orm.api.state.tweetMeme_index = index - 1
