from controller.throttle.decoder import Decoder


class Data:


    def __init__(self):
        self.decoder  = Decoder()
        self.genericM = '\u00AC\u2203\u03BC    \u2234 awaiting signal-\u03F4'
        self.messages = dict.fromkeys([
            "follower", "following", "friend", "unfriend", "reply_type1",
            "reply_type2", "tweet", "type_alpha", "type_lambda", "quantum",
            "youtube", "blog", "inactive", "destroyer", "mention"
            ], self.genericM)
        self._stat    = dict.fromkeys([
            "friend", "unfriend", "follower", "following", "tweet", 
            "type_alpha", "unfriendQ", "friendQ"], 0)
        self.params   = {"replied": False}

        """
        messages = dict.fromkeys([
            "follower", "following", "friend", "unfriend", "like",
            "reply", "tweet", "type_alpha", "query", "quantum",
            "youtube", "blog", "inactive", "destroyer", "mention"
            ])
        """

    def get(self, admin):
        self._parse(admin)
        return self.messages


    def stats(self, admin):
        for param in ("name", "tweetQ"):
            try: self._stat.pop(param)
            except KeyError: pass
        for key in self._stat.keys():
            count = getattr(admin.orm.api.state, f"{key}_count")
            self._stat[key] = count
        self._stat["tweetQ"] = self._tweetQ_count(admin)
        self._stat["name"]   = admin.name
        return self._stat

    
    def _tweetQ_count(self, admin):
        self.params.update({"type": "reply_type1"})
        count  = admin.orm.api.tweets.count(**self.params)
        self.params.update({"type": "reply_type2"})
        count += admin.orm.api.tweets.count(**self.params)
        return count


    def _parse(self, admin):
        self.decoder.admin = admin
        admin.orm.api.messages.get()
        for message in admin.orm.api.messages:
            data, process = message.data, message.process
            if process not in self.messages: continue
            try: data, process = self.decoder(data, process)
            except (TypeError, AttributeError, AssertionError): pass
            self.messages[process] = data or self.genericM
