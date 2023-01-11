from model.objects.exceptions import MonthlyRateLimitException
from model.objects.exceptions import UnhandledHTTPException
from model.objects.exceptions import RateLimitException
from model.objects.exceptions import ForbiddenException
from model.objects.exceptions import ProtectedException
from datetime import timedelta
from datetime import datetime
import traceback
import logging
import random


log = logging.getLogger(__name__)


class SuperManager:


    def execute(self):
        raise NotImplementedError


    def _handler(self, **params):
        r = None
        try:
            r = self.admin.twitter.api(self, self.admin, **params)
            assert r.status_code == 200
        except MonthlyRateLimitException as HTTP_429:
            self._set_timestamp(60 * 24)
            self.report(f"{self.name.title()} operation sleeping 24 hours "
                        f"because monthly rate limit.")
            raise MonthlyRateLimitException
        except RateLimitException as HTTP_429_or_HTTP_503:
            if (self.name == "retweets"):
                raise RateLimitException(429)
            elif (self.name == "reply_type1"):
                n = random.randint(15, 60)
                self._set_timestamp(n)
            else:
                self._set_timestamp()
            self.report(f"{self.name.title()} operation sleeping because rate "
                         "limit.")
            raise RateLimitException(429)
        #except ForbiddenException as HTTP_403:
        #    raise ForbiddenException
        except AssertionError as HTTP_400:
            self.report(f"HTTP 400: {self.name}")
            raise ProtectedException(400)
        except (UnhandledHTTPException, AttributeError):
            e = traceback.format_exc()
            log.debug(f"{self.admin.name}\n{e}")
            self._set_timestamp()
            raise UnhandledHTTPException
        else:
            return r


    def _set_timestamp(self, minutes = 15, seconds = None, name = None):
        if (self.name == "retweets"):
            attr = "like_delta"
        else:
            attr = self.name + "_delta"
        if seconds:
            timestamp = datetime.utcnow() + timedelta(seconds = seconds)
        else:
            timestamp = datetime.utcnow() + timedelta(minutes = minutes)
        setattr(self.admin.orm.api.state, attr, timestamp)


    def _get_pagination(self):
        return getattr(self.admin.orm.api.state, f"{self.name}_pagination")


    def delta(self, alpha, zeta):
        t = datetime.utcnow() + timedelta(seconds = random.randint(alpha, zeta))
        return t


    def report(self, message, name = None):
        self.admin.orm.api.messages.create(message, name or self.name)
        log.info(f"{self.admin.name}\n{message}")
