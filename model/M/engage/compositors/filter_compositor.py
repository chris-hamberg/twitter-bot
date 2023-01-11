import logging
import os


log = logging.getLogger(__name__)


class FilterCompositor:

    
    def __init__(self, admin):
        self.admin = admin
        self.refresh_keywords()
        self.refresh_blacklist()
        self.refresh_blacklisted_users()


    def filter(self, text, name = None, user = None, username = None, 
            mentions = False):

        try:
            text, state, message = text.lower(), False, str()
            user = user or username
        except AttributeError:
            text, state, message = text[1].lower(), False, str()
            user = name

        if user:
            for blacklisted in self._blacklisted_users:
                if user.lower() in blacklisted.lower():
                    return True

        if not mentions:
            for keyword in self._keywords:
                if " " + keyword in text:
                    #message = f"Tweet contains '{keyword}'."
                    #self.admin.orm.api.messages.create(message, name)
                    #log.debug(f"{self.admin.name}\n{message}")
                    break
            else:
                #message = f"Tweet does not contain keywords for engagement."
                state = True
    
        if not state:
            for blacklisted in self._blacklist:
                if " " + blacklisted in text:
                    #message = f"Tweet contains blacklisted keywords."
                    state = True
                    break

        return state


    def refresh_keywords(self):
        path = os.path.join("tweets", f"{self.admin.username}", 
                "retweet_keywords.txt")
        if os.path.exists(path):
            with open(path, "r") as fhand:
                keywords = fhand.read()
            self._keywords = keywords.rstrip().split("\n")
        else:
            self._keywords = []


    def refresh_blacklist(self):
        path = os.path.join("tweets", f"{self.admin.username}", 
            "retweet_blacklist.txt")
        if os.path.exists(path):
            with open(path, "r") as fhand:
                blacklist = fhand.read()
            self._blacklist = blacklist.rstrip().split("\n")
        else:
            self._blacklist = []


    def refresh_blacklisted_users(self):
        path = os.path.join("tweets", f"{self.admin.username}",
                "username_blacklist.txt")
        if os.path.exists(path):
            with open(path, "r") as fhand:
                blacklist = fhand.read()
            self._blacklisted_users = blacklist.rstrip().split("\n")
        else:
            self._blacklisted_users = []
