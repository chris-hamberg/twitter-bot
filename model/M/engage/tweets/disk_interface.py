import random
import os


class DiskInterface:


    def __init__(self, admin):
        self.admin = admin

        self._directory = os.path.join("tweets", f"{self.admin.username}")

        self._hardcoded_tweets = os.path.join(
                self._directory, "tweets.txt")

        self._media_ids        = os.path.join(
                self._directory, "meme_ids.txt")

        self._media_header     = os.path.join(
                self._directory, "meme_header.txt")


    def get_tweet(self):
        path = self._hardcoded_tweets
        with open(path, "r") as fhand:
            data   = fhand.read()
            tweets = data.split("#tweet#")
            if (tweets[-1] == "\n"):
                tweets = tweets[:-1]
        tweet = random.choice(tweets)
            #if (len(tweets) <= self.admin.orm.api.state.tweetHardcoded_index):
            #    self.admin.orm.api.state.tweetHardcoded_index = 0
            #tweet = tweets[self.admin.orm.api.state.tweetHardcoded_index]
        return tweet


    def get_meme(self):
        path  = self._media_ids
        index = self.admin.orm.api.state.tweetMeme_index
        with open(path, "r") as fhand:
            media_ids = fhand.read()
            media_ids = media_ids.rstrip().split("\n")
        if (len(media_ids) <= index):
            self.admin.orm.api.state.tweetMeme_index = index = 0
        if (index == 0):
            media_ids = self._sort_memes(media_ids, path)
        media = media_ids[self.admin.orm.api.state.tweetMeme_index]
        text  = self._get_meme_text()
        return text, media


    def _sort_memes(self, media_ids, path):
        last = media_ids[0]
        media_ids = media_ids[1:]
        random.shuffle(media_ids)
        media_ids = media_ids + [last]
        media_ids_document = "\n".join(media_ids)
        with open(path, "w") as fhand:
            fhand.write(media_ids_document)
        return media_ids

    
    def _get_meme_text(self):
        path = self._media_header
        with open(path, "r") as fhand:
            header = fhand.read()
        return header
