from model.M.engage.tweets.disk_interface import DiskInterface
from model.M.engage.tweets.tweet_maker_ai import TweetMakerAI
from model.objects.exceptions import ConfigurateXType1Ex
from model.objects.exceptions import ConfigurateXType2Ex
from model.objects.exceptions import ConfigurateXType3Ex
from model.M.engage.hybridization import Hybridization
import logging
import random
import time
import os


log = logging.getLogger(__name__)


class TweetPreprocessor:


    def __init__(self, admin):
        self.admin  = admin
        self.disk   = DiskInterface(admin)
        self.ai     = TweetMakerAI(admin)
        self.hybrid = Hybridization(admin)
        self.method = {
                "stream" : self._get_video,   "playlist": self._get_video,
                "static" : self._get_tweet,   "meme"    : self._get_tweet, 
                "blog"   : self._get_article, "tweetAI" : self._get_tweetAI}
        path = os.path.join("model", "M", "engage", "tweets", 
                "emojis_choices.txt")
        with open(path, "r") as fhand:
            emojis_choices = fhand.read()
        self.emojis_choices = emojis_choices.replace("\\n", "\n")
        self.emojis_choices = emojis_choices.split(",")
        try: self.emojis_choices.remove("")
        except ValueError: pass


    def get(self, type):
        tweet, media, url, protocol = self.method[type](type)
        if   (type == "blog"   ): return tweet, url, protocol
        elif (type == "tweetAI"): return tweet
        elif (type == "static" ): return tweet
        else:                     return tweet, media


    def _get_video(self, type):
        try:
            videos = self.admin.orm.api.youtube.read(type = type,posted = False)
            media  = random.choice(videos)
            tweet  = self._format_video(media)
        except (IndexError, TypeError): raise ConfigurateXType3Ex
        return tweet, media, None, None


    def _get_tweet(self, type):
        try:
            media = None
            if (type == "static"):
                tweet = self.disk.get_tweet(); assert tweet
                tweet = self._format_tweet(tweet, type = type)
            else:
                tweet, media = self.disk.get_meme()
                assert tweet; assert media
                tweet = self._format_tweet(tweet)
            return tweet, media, None, None
        except AssertionError: raise ConfigurateXType3Ex


    def _get_article(self, type):
        try:
            feeds         = self.admin.orm.api.blog.read(posted = False)
            feed          = feeds[0]
            title         = feed[4]
            protocol, url = feed[3].split("://")
            tweet         = f"{title}\n{url}"
            return tweet, None, url, protocol
        except IndexError: raise ConfigurateXType2Ex


    def _get_tweetAI(self, type):
        params = {"liked": False, "replied": False, "mentioned": False}
        params.update({"type": "tweetAI"})
        if (self.admin.orm.api.tweets.count(**params) < 3):
            self._get_ai_tweet()
        tweets = self.admin.orm.api.tweets.read(**params)
        if (not tweets): raise ConfigurateXType1Ex
        return random.choice(tweets), None, None, None
        

    def _format_video(self, video):
        title, url, emojis = video[5], video[6], bool(video[7])
        if (not emojis) or (random.random() < 0.33):
            emojis = str()
        elif emojis:
            e = random.choice(video[7].split(","))
            length = random.randint(1, 4)
            emojis = e * length

        if emojis:
            choice  = random.choice(self.emojis_choices)
            choice  = choice.replace("\\n", "\n")
            choice  = choice.format(title=title, url=url, emojis=emojis)
        else:
            choices = [f"\n{title}\n\n{url}", f"\n{title}\n\n{url}\n",
                       f"\n{title}\n{url}", f"\n{title}\n{url}\n", 
                       f"{title}\n\n{url}", f"{title}\n\n{url}\n", 
                       f"{title}\n{url}", f"{title}\n{url}\n"]
            choice = random.choice(choices)
        return choice


    def _format_tweet(self, tweet, delimiter = "\n\n", type = None):
        while ((tweet.find("{{") != -1) and (tweet.find("}}") != -1)):
            start, end = tweet.find("{{"), tweet.find("}}")
            choices = tweet[start+2:end].replace("\n", "").split("||")
            choice  = random.choice(choices)
            tweet   = tweet[:start] + choice + tweet[end+2:]

        if (type == "static"):
            temp, tweet = tweet.split("\n"), list()
            while True:
                try:
                    temp.remove("")
                except ValueError:
                    break
            for part in temp[:-1]:
                tweet.append(part)
                tweet.append("\n")
            tweet.append(temp[-1])
            temp = tweet[1:]
            random.shuffle(temp)
            tweet = [tweet[0]] + temp
            for e, part in enumerate(tweet[1:]):
                e += 1
                if tweet[e - 1].endswith("\n"):
                    continue
                tweet[e] = " " + tweet[e]
            tweet = "".join(tweet)
        else:
            tweet = tweet.split("\n")
            tweet = delimiter.join(tweet)[:-2]
        tweet = tweet.encode("UTF-8").decode("unicode-escape")
        return tweet


    def _get_ai_tweet(self):
        self.hybrid.monitor("tweet")
        params  = {"liked": False, "replied": False, "mentioned": False}
        params.update({"type": "tweetAI"})
        message = ("AI is generating at least 3 tweets. (This takes "
                   "several minutes.)")
        self.admin.orm.api.messages.create(message, "tweet")
        log.debug(f"{self.admin.name}\n{message}")
        time.sleep(3)
        self.ai.generate()
        if (self.admin.orm.api.tweets.count(**params) < 3):
            self._get_ai_tweet()
        self.hybrid.close()

