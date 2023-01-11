from model.objects.exceptions import ProtectedException
from model.objects.exceptions import ForbiddenException

from model.M.super.superclass import SuperManager

import logging
import pickle
import random
import time


log = logging.getLogger(__name__)


class LikeCompositor(SuperManager):


    def __init__(self, admin):
        self.params = {"admin_id":admin.id, "auth":admin.auth}
        self.admin  = admin
        self.name   = "like"


    def tweets_by_ids(self, ids, name, mentions = False):
        for id in ids:
            self.params.update({"tweet_id": str(id)})
            try:
                r = self._handler(**self.params)
            except (ProtectedException, ForbiddenException):
                message = f"Tweet {id} is most likely protected. Cannot like."
                self.admin.orm.api.messages.create(message, name)
                log.debug(f"{self.admin.name}\n{message}")
                continue
            finally:
                self.params.pop("tweet_id")
            self._postprocess(id, name)


    def _postprocess(self, id, name):
        t = random.randint(1, 3)
        self._update_state()
        self._report(id, t, name)
        time.sleep(t)


    def _update_state(self):
        count = self.admin.orm.api.state.like_count + 1
        self.admin.orm.api.state.like_count = count


    def _report(self, id, t, name):
        message = f"Liked tweet {int(id)}."
        self.admin.orm.api.messages.create(message, name)
        log.info(f"{self.admin.name}\n" + message)
