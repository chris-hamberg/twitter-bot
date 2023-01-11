from model.objects.exceptions import ConfigurateXType1Ex
from transformers import pipeline
import traceback
import logging
import random
import os


log = logging.getLogger(__name__)


class TweetMakerAI:

    FLAGS = [ 
              " don#t know", " know nothing",
              "i haven#t heard", " we", " our", " us ", "i don#t like", 
              "i don#t really like", "i don#t even like", " free",
              "i don#t think", "m a new", 
              "m a little lost", "m lost", "male", " giv",
              " old ", " -old", "m not ", "not my", 
              "i recently started", "my name",
              "people like that", "i don#t have any business", 
              "you don#t get", "you are", "you#re", "problem with my", 
              "you can#t get much", "why are you", "you#re not", 
              "you#re probabily not",
              "i need to know", "i have never", 
              "i have no interest", "i own", "don't even have", 
              "never", "make people think",
              "it#s not", "it is not", "i use them", "not good", "not a good",
              "not very good", "video", "to beat", "first", "second", "third", 
              "next", "you need", "you don#t", "you do not", "angry", "prick",
              "shit", "fuck", "bitch", " ass", "i can#t", " list", "years", 
              "to you", " mom", " dad",
              "husband", "wife", "click", "buy them", "buy it", "i don#t",
              "read the comments", "previous post", "i#m a woman", "i#m a man",
              "i am a woman", "i am a man", " man", " woman", "go on a date", 
              "love", "waste your time", "i just couldnt", "i just couldn#t",
              "i couldnt", "i couldn#t", "wrong with my", 
              "i#m about to learn", "i am about to learn", "i#m learning",
              "i am learning", "learning", "you can#t", "i live in", "i am from", 
              "too hard", "no skill", "i have no", "i#m only a ", "young man",
              "young woman", "girl", " boy", "download", "not as good",
              "i am no", "i#m no", "area", "the same", "father", "mother",
              "economy", "section above", "You page", "website", " site", 
              " page", " webpage", "i do not", "decade", " guy", "for him",
              "for her", "showing you how", "show you how", "teach me",
              "company called", "archives", "i#m try", "i am try", 
              "not the best", " sorry", " org", " partner", "i haven#t",
              "i have not", "raised in", " begun", " beginner", " novice",
              "you still can#t", "you still cannot", "you still can not",
              "i still can#t", "i still cannot", "i still can not", 
              "i#ve started", "i have started", "i used to be", "baby",
              "you have no", "i want to be", " youth", " hate", " article"]


    START_FLAGS = ["But ", "And ", "We ", "We#ve ", "Our ", "Us ", "Free ", 
            "Give ", "Giving ", "Be ", "I also ", "I am also ", "I#m also ", 
            "However ", "He ", "He#s ", "She ", "She#s ", ") ", "They ", 
            "They#ve ", "They#re ", "For example ", "This is ", "I use them ", 
            "Not to mention ", "It is", "It#s ", "It was ", "In the sense ", 
            "That#s ", "That is ", "I use it ", "Which is why ", 
            "I don#t ", "It ", "com ", "We#re ", "The ",
            "So ", "Here#s ", "Here is", "What#s wrong with ", "Not for ",
            "Not just for ", "You have no ",
            "I#m about to learn ", "I am about to learn ", "I#m learning ",
            "I am learning ", "You can#t", "I think you can use this to",
            "You can use this to ", "I have no ", "For this reason, ",
            "For that reason, ", "I#m only a ", "I try to ",
            "I#m going to do it ", "Because ", "You can also ", "You also ",
            "Not only that, ", "I am talking about ", "I#m talking about ",
            "That ", "This ", "The rest ", "and ", "By contrast, ", 
            "For instance, ", "In a recent interview ", "I#m trying ",
            "I am trying ", "In some cases, ", "What I was about to tell you ",
            "By the way, ", "Now ", "A way ", "As for ", "In addition, ",
            "In addition ", "On the other hand, ", "I#ve started ",
            "I have started ", "About Me ", "I want to be ", "In fact, ", 
            "Like I was saying, ", "As I was saying, "]


    PRONOUNS = ["they", "them", " it is", " it was", " it#s", " their", " this", 
            "that#s", "that", "i use it", " here#s", " here is", "those", " it", 
            "these", " his ", " her ", " he ", " he#", " she ", " she# ",
            " also", " it ", " thing ", " though", " too", " the ", " some are"]


    GLOBAL_FLAGS = ["monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday", "january", "february", "march", "april",
            "june", "july", "august", "september", "october", "november",
            "december", " 190", " 191", " 192", " 193", " 194", " 195", " 196", 
            " 197", "198", " 200", " 201", " 202", "@", "$", 
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "(", ")",
            "russia"]


    def __init__(self, admin, test = False):
        self._admin    = admin
        self._model    = "EleutherAI/gpt-neo-125M"       
        replacements   = self._get_fdata(admin, "tweetAI_replacements")
        self._prompts  = self._get_fdata(admin, "tweetAI_prompts")
        self._keywords = self._get_fdata(admin, "retweet_keywords")
        self._test     = test
        self._parseR(replacements)


    def generate(self, test = False):

        try:
            index = self._admin.orm.api.state.tweetAI_prompt_index
            if len(self._prompts) <= index:
                self._admin.orm.api.state.tweetAI_prompt_index = index = 0
            self._prompt = self._prompts[index]
            assert self._keywords, "engagement_keywords.txt"
        except (IndexError, AssertionError) as error:
            message = "AI cannot write tweets without first configuring "
            if error.args: message += error.args[0]
            else:          message += "tweetAI_prompts.txt"
            self._admin.orm.api.messages.create(message, "tweet")
            log.debug(f"{self._admin.name}\n{message}")
            time.sleep(3)
            raise ConfigurateXType1Ex(message)
        

        #elif (not test):
        self._report("TweetMakerAI Initializing.")
        pipe = pipeline("text-generation", model = self._model)
        self._report("TweetMakerAI generating tweet(s) (this takes several "
                     "minutes.)")
        r = pipe(self._prompt, do_sample = True, top_k = 60, temperature = 0.72,
                max_length = 40 + len(self._prompt), num_return_sequences = 100)


        tweets = self._parse(r)
        tweets = list(set(tweets))
        tweets = self._replace(tweets)
        tweets = self._validate(tweets)
        tweets = self._filter_type5(tweets)
        tweets = self._filter_type6(tweets)
        if (not bool(tweets)): tweets = self.generate()
        tweets = self._format_tweets(tweets)
        self._admin.orm.api.state.tweetAI_prompt_index = index + 1
        return tweets


    def _format_tweets(self, tweets):
        x, y, xQ = 0, 99999999999999, []
        database  = self._admin.orm.api.tweets.read()
        tweet_ids = [tweet[0] for tweet in database]
        for tweet in tweets: 
            while True:
                try:
                    tweet_id = random.randint(x, y)
                    tweet_ids.index(tweet_id)
                except ValueError: break
            text            = f"{tweet}."
            id              = self._admin.id
            admin           = self._admin.id
            type            = "tweetAI"
            query           = None
            conversation_id = None
            tweet = (tweet_id, text, id, admin, type, query, conversation_id)
            xQ.append(tweet)
        self._admin.orm.api.tweets.create(xQ)
        message = f"TweetMakerAI created {len(xQ)} tweets."
        self._admin.orm.api.messages.create(message, "tweet")
        log.debug(f"{self._admin.name}\n{message}")


    def _get_fdata(self, admin, fname):
        path = os.path.join("tweets", admin.username, f"{fname}.txt")
        with open(path, "r") as fhand:
            fdata = fhand.read()
            fdata = fdata.rstrip().split("\n")
            if str() in fdata: fdata.remove(str())
        return fdata


    def _report(self, message):
        if not self._test: 
            log.debug(f"{self._admin.name}\n{message}")
            self._admin.orm.api.messages.create(message, "tweet")
        else: print(message)


    def _parse(self, r):
        tweets = []
        for i, _ in enumerate(r):
            text = ".".join(r[i].get("generated_text").split(".")[1:-1])
            text = " ".join(text.split())
            text = text.replace(r'"', str())
            text = text.replace(r'“', str())
            text = text.replace(r'”', str())
            text = text.split(".")
            while text:
                n           = random.randint(1, len(text))
                tweet, text = text[:n], text[n:]
                tweet       = self._filter_type2(tweet)
                if  tweet: 
                    tweet   = self._filter_type3(tweet)
                if  tweet:
                    tweet   = self._filter_type4(tweet)
                    tweet   = ".".join(tweet)
                    if not self._filter_type1(tweet):
                        tweet = tweet.lstrip("(")
                        if "." in tweet[:10]: pass
                        else: tweets.append(tweet)
                del tweet
        return tweets


    def _parseR(self, replacements):
        self._replacements = []
        for replacement in replacements:
            t = old, new = replacement.split(",")
            self._replacements.append(t)


    def _filter_type1(self, text):
        for flag in self.__class__.GLOBAL_FLAGS:
            if (flag.lower() in text.lower()): return True
        for keyword in self._keywords:
            if text.lower().count(keyword.lower()):
                return False
        return True


    def _filter_type2(self, tweet):

        while True:
            try: tweet.remove(str())
            except ValueError: break

        while True:
            try: tweet.remove(" ")
            except ValueError: break

        if (not tweet): return False

        try:
            while (tweet[0][0] == " "): tweet[0] = tweet[0][1:]
        except IndexError:
            e = traceback.format_exc()
            log.debug(f"{self._admin.name}\n{e}")
        xQ, i = self.__class__.START_FLAGS, 1
        start = tweet[0]
        start = start.split()
        while i < 3:
            sigma = start[:i]
            sigma = " ".join(sigma)
            sigma = sigma.replace("'", "#")
            sigma = sigma.replace("’", "#")
            sigma = sigma.replace("’", "#")
            if   sigma            in xQ: return False
            elif sigma      + " " in xQ: return False
            elif sigma[:-1] + " " in xQ: return False
            elif sigma[:-2] + " " in xQ: return False
            i += 1
        else: return tweet


    def _filter_type3(self, tweet):
        i, Q = 0, []
        while i < len(tweet):
            filter = self._sentence_filter(tweet[i])
            if ((not i) and (filter)): return False
            elif (not filter): Q.append(tweet[i])
            i += 1
        return Q if Q else False
        

    def _filter_type4(self, tweets):

        for e, tweet in enumerate(tweets):
            if tweet.startswith(" "):
                tweets[e] = tweet[1:]

        for e, tweet in enumerate(tweets):
            i = 1
            while True:
                try: 
                    i = (e + i)
                    i = tweets[i:].index(tweet) + i
                    tweets[i] = None
                except ValueError: break

        try:
            while (None in tweets): tweets.remove(None)
        except ValueError: pass

        for e, _ in enumerate(tweets[1:]):
            tweets[e + 1] = " " + tweets[e + 1]

        return tweets


    def _filter_type5(self, tweets):
        xQ = []
        for tweet in tweets:
            phi = tweet.split(".")[0]
            phi = phi.replace("'", "#")
            phi = phi.replace("’", "#")
            for pronoun in self.__class__.PRONOUNS:
                if phi.lower().count(pronoun.lower()):
                    break
            else: xQ.append(tweet)
        return xQ


    def _filter_type6(self, tweets):
        xQ = []
        for tweet in tweets:
            if tweet[0].isupper(): xQ.append(tweet)
        return xQ



    def _sentence_filter(self, sentence):
        sentence = sentence.replace("'", "#")
        sentence = sentence.replace("’", "#")
        for flag in self.__class__.FLAGS:
            if sentence.lower().count(flag.lower()): return True
        else: return False


    def _replace(self, tweets):
        result = []
        for tweet in tweets:
            words = tweet.split()
            for i, word in enumerate(words):
                title = False
                if word.istitle(): title = True
                if word[-1].lower() == "s":
                    word = self._replacements.get(word[:-1].lower(), word) + "s"
                else:
                    word = self._replacements.get(word.lower(), word)
                if title: word = word.title()
                words[i] = word
            tweet = " ".join(words).strip()
            result.append(tweet)
        return result


    def _replace(self, tweets):
        for i, tweet in enumerate(tweets):
            for old, new in self._replacements:
                tweet = tweet.replace(old, new)
                tweet = tweet.replace(
                        old[0].title() + old[1:], 
                        new[0].title() + new[1:])
            tweets[i] = tweet
        return tweets


    def _validate(self, tweets):
        result = []
        for tweet in tweets:
            if len(tweet) <= 140: result.append(tweet)
        return result


if __name__ == "__main__":
    import pickle, sys
    sys.path.append(os.getcwd()) 
    from model.orm.api.users.administrators import Administrators
    db = "model/data.db"
    admins = Administrators(db)
    admin  = admins[0]
    ai = TweetMakerAI(admin, test = True)
    if sys.argv[1:]:
        test = sys.argv[1]
    else:
        test = False
    ai.generate(test = test)
