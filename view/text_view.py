from model.orm.api.users.administrators import Administrators
from model.objects.normalize import normalize
from view.text_animation import TextAnimation
from controller.data import Data
from datetime import timedelta
from datetime import datetime
import random
import sys
import os


class TextView:


    def __init__(self, db, multiproc = True):
        self.animation  = TextAnimation(db)
        self.admins     = Administrators(db)
        self.data       = Data()
        self._display   = dict()
        self._multiproc = multiproc


    def show(self):
        display = str()
        for e,   _ in enumerate(self.admins): self._build(e)
        for key, _ in enumerate(self._display): display += self._display[key]
        if self._multiproc: self._clear()
        print(display)


    def _clear(self):
        if "win" in sys.platform: os.system("cls")
        else: os.system("clear")


    def _build(self, e):

        stats    = self.data.stats(self.admins[e])
        data     = self.data.get(self.admins[e])
        messages = dict()

        for key, val in data.items():
            messages[key] = self.animation.animate(e, val, key)

        pad1 = "-" * len(stats.get('name')) + "   "
        pad2 = " " * len(stats.get('name')) + "   "
        #NOTE
        if e == 1:
            pad1 += "    "
            pad2 += "    "

        
        self._display[e] = f"""{stats.get('name')}        Followers: {stats.get('follower'): 8,}    Following: {stats.get('following'): 8,}    Tweets:     {stats.get('tweet'): 8,}
{pad1}     Friended:  {stats.get('friend'): 8,}    Unfriended:{stats.get('unfriend'): 8,}    TweetQ:     {stats.get('tweetQ'): 8,}
{pad2}     FriendQ:   {stats.get('friendQ'): 8,}    UnfriendQ: {stats.get('unfriendQ'): 8,}    Scraper:    {stats.get('type_alpha'): 8,}
       
 User Management
   QuantumP.Reactor ::: {messages['quantum']}
   Follower ::::::::::: {messages['follower']}
   Following :::::::::: {messages['following']}
   Inactive Followers : {messages['inactive']}

   Friend ::::::::::::: {messages['friend']}
   Unfriend ::::::::::: {messages['unfriend']}
 
 Social Media Engagement
  - Reply (type-α) :::: {messages['reply_type1']}
  - Reply (type-β) :::: {messages['reply_type2']}
  - Mention ::::::::::: {messages['mention']}
  Tweet ::::::::::::::: {messages['tweet']}

 Data Management
  Enforcer :::::::::::: {messages['destroyer']}
  Type-Alpha :::::::::: {messages['type_alpha']}
  Type-λ :::::::::::::: {messages['type_lambda']}
  YouTube ::::::::::::: {messages['youtube']}
  RSSParser ::::::::::: {messages['blog']}"""
