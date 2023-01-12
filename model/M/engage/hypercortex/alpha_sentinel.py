from model.M.super.reporter import Reporter
from difflib import SequenceMatcher
from math import ceil
import logging
import random
import os


log = logging.getLogger(__name__)


class AlphaSentinel:


    def __init__(self, admin, name):
        self.reporter = Reporter(admin, name)
        self.admin    = admin
        self.update_blacklist()


    def type_1(self, instruction):
        if bool(instruction): return False
        self.reporter.report("HyperCortex (type-α) AI requires instruction.")
        return True


    def type_2(self):
        if (15 <= self.admin.orm.api.state.reply_count): return True
        else: return False


    def type_3(self, dialog, t_id):
        length      = ceil(len(dialog) / 2) - 1
        probability = 100 - (length * 15)
        p           = round(random.random() * 100, 2)
        if (p <= probability): return False
        self.admin.orm.api.tweets.update(t_id)
        return True


    def type_4(self, response):
        for blacklisted in self._blacklist: 
            if (not response.lower().count(blacklisted.lower())): continue
            self._debug(f"AI response contains: {blacklisted}")
            return True
        return False


    def type_5(self, response):
        if 140 < len(response): return True
        else: return False


    def type_6(self, response, ptweet):
        p = SequenceMatcher(None, response, ptweet).ratio()
        if (p < 0.4): return False
        self._debug(f"0.4 <= {p}\nresponse: {response}\ninput: {ptweet}")
        return True


    def update_blacklist(self):
        p = ["tweets", f"{self.admin.username}", "replyAI_blacklist.txt"]
        p = os.path.join(*p)
        with open(p, "r") as fhand: blacklisted = fhand.read()
        blacklisted = blacklisted.split("\n")
        try: blacklisted.remove("")
        except ValueError: pass
        self._blacklist = blacklisted


    def _debug(self, message): log.debug(f"{self.admin.name}\n{message}")
