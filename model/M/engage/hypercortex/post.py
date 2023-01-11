from model.M.engage.reply.type2 import ReplyType2Manager
from model.M.super.reporter import Reporter
import random
import time


class Post:


    def __init__(self, admin, name):
        self.reporter = Reporter(admin, name)
        self.reply    = ReplyType2Manager(admin)
        self.admin    = admin
        self.retries  = 5
        self.kwgs     = {"reply_chance": 100}


    def send(self, c_id, t_id, response):
        self.kwgs.update({"text": response, "tweet_id": str(t_id)})
        while self.retries:
            r = self.reply._reply(**self.kwgs)
            if self.validate(r, c_id, response): break
            else: self.retries -= 1; time.sleep(random.randint(2, 6))


    def HTTP2xx(self, r, c_id, response):
        count = self.admin.orm.api.state.reply_count
        self.admin.orm.api.state.reply_count = count + 1
        self.reply._record(r, [c_id])
        return f"HTTP {r.status_code}: {response}", True


    def HTTP403(self, r):
        message  = f"HTTP {r.status_code}"
        if not r.json().get("errors"): return message, False
        error    = r.json().get("errors")[0].get("message")
        if not "community tweet" in error.get("detail"): return message, False
        detail   = error.get("detail")
        message += f": {detail}"
        return message, True


    def HTTPxxx(self):
        message  = f"HTTP {r.status_code}"
        if not r.json().get("errors"): return message, False
        error    = r.json().get("errors")[0].get("message")
        message += f": {error}"
        return message, False


    def mangled(self): return "Fatal error in trying to send the reply.", False


    def validate(self, r, c_id, response):
        if not r:                    message, _break = self.mangled()
        elif (r.status_code == 403): message, _break = self.HTTP403(r)
        elif (200 <= r.status_code < 300):
            message, _break = self.HTTP2xx(r, c_id, response)
        else: message, _break = self.HTTPxxx()
        self.reporter.report(message)
        return _break
