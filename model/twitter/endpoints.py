from model.objects.exceptions import MonthlyRateLimitException
from model.objects.exceptions import UnhandledHTTPException
from model.objects.exceptions import NoInternetException
from model.objects.exceptions import RateLimitException
from model.objects.exceptions import ForbiddenException

from model.twitter.lookup_username import LookupUsername
from model.twitter.friend_request import FriendRequest
from model.twitter.friend_delete import FriendDelete
from model.twitter.search_tweets import SearchTweets
from model.twitter.followers import Followers
from model.twitter.lookup_me import LookupMe
from model.twitter.retweet import Retweet
from model.twitter.type_alpha import ScraperTypeAlpha
from model.twitter.follows import Follows
from model.twitter.likes import Like

import traceback
import requests
import logging
import sqlite3
import pickle
import random
import json
import time
import sys


log = logging.getLogger(__name__)


class Endpoints:


    def __init__(self, admin):
        self.admin = admin
        self.msg   = "HTTP {code} {admin} {name} {proto}"


    def __call__(self, caller, admin, **kwargs):
        protocol = self.selector(caller, admin, **kwargs)
        return self.handler(caller, admin, protocol, **kwargs)


    def selector(self, caller, admin, **kwargs):

        if caller.__class__.__name__ == "Administrator":
            #if kwargs.get("username"):
            #    protocol = LookupUsername()
            #else:
            protocol = LookupMe()

        elif hasattr(caller, "name"):

            match caller.name:

                case "follower":
                    protocol = Followers()

                case "following":
                    protocol = Follows()

                case "type_alpha":
                    protocol = ScraperTypeAlpha()

                case "friend":
                    protocol = FriendRequest()

                case "unfriend":
                    protocol = FriendDelete()

                case "type_lambda":
                    protocol = SearchTweets()

                case "like":
                    protocol = Like()

                case "retweets":
                    protocol = Retweet()

        elif kwargs.get("username"):
                protocol = LookupUsername()

        return protocol


    def handler(self, caller, admin, protocol, **kwargs):

        name = caller.__class__.__name__
    
        code, retries, proto = 0, 3, protocol.__class__.__name__

        if not admin:
            admin = "n/a"

        while (((code != 200) or (code != 201)) and bool(retries)):
            try:
                r = protocol.request(**kwargs)
                code = r.status_code
                retries -= 1
                if (code == 429):
                    self.report(code, admin, name, proto, caller)
                    if ((r.json().get("title") == "UsageCapExceeded") and (
                            r.json().get("period") == "Monthly")):
                        raise MonthlyRateLimitException
                    else:
                        raise RateLimitException
                elif (code == 503):
                    self.report(code, admin, name, proto, caller)
                    if (caller.name == "like"):
                        raise ForbiddenException
                    raise RateLimitException
                elif (code == 403):
                    #self.report(code, admin, name, proto, caller)
                    #log.debug(403)
                    import pdb; pdb.set_trace()
                    raise ForbiddenException
                elif (code == 400):
                    if r.json().get("errors"):
                        e = r.json().get("errors")[0].get("message")
                        log.debug(e)
                        if (caller.name == "type_lambda"):
                            if "must be a tweet id" in e:
                                kwargs.pop("since_id")
                                continue
                    else:
                        self.report(code, admin, name, proto, caller)
                    return r
                elif (code == 200) or (code == 201): 
                    return r
                else:
                    time.sleep(1)
            except requests.exceptions.ConnectionError:
                e = traceback.format_exc()
                log.debug(e)
                if hasattr(caller, "name"):
                    self.admin.orm.api.messages.create("Connection Error.", caller.name)
                    log.debug(f"{proto.__class__.__name__}")
                raise requests.exceptions.CennectionError
            except requests.exceptions.SSLError:
                e = traceback.format_exc()
                log.debug(e)
                if hasattr(caller, "name"):
                    self.admin.orm.api.messages.create("SSL Error.", caller.name)
                    log.debug(f"{proto.__class__.name}")
                raise requests.exceptions.SSLError
        if ((code != 200) or (code != 201)):
            self.report(code, admin, name, proto, caller)
            raise UnhandledHTTPException(f"{r.status_code}")


    def report(self, code, admin, name, proto, caller):

        if isinstance(admin, str):
            n = admin
        else:
            n = admin.name
       
        try:
            m = self.msg.format(code = code, admin = self.admin.name, 
                    name = name, proto = proto)
        except (RecursionError, sqlite3.OperationalError, AttributeError):
            e = traceback.format_exc()
            log.debug(e)
            return False

        log.info(m)

        m = " ".join(m.split(" ")[:2])

        if ((admin != "n/a") and (hasattr(caller, "name"))):
            self.admin.orm.api.messages.create(m, caller.name)
        elif (admin != "n/a"):
            self.admin.orm.api.messages.create(m, proto)
        else:
            self.admin.orm.api.messages.create(m, proto)
