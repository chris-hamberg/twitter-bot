from model.objects.normalize import normalize
from datetime import datetime


class Decoder:


    def __init__(self):
        self._method = {
                "friend"       : self._friend,
                "tweet"        : self._tweet,
                "type_epsilon" : self._scraper_type_epsilon,
                "inactive"     : self._inactive,
                "type_gamma"   : self._type_gamma
                }


    def __call__(self, data, name, database = False):
        if self._sentinel(data, name): return data, name
        name, message, seconds = self._cases(name)
        try: message = self._method[name](message, seconds)
        except KeyError: pass
        finally: return self._store(message, name, database)

    
    def _sentinel(self, data, name):
        assert data.count("rate limit") or data.count("asleep")
        if   (name == "reply_type2") and data.count("asleep"): return True
        elif (name == "tweet")       and data.count("asleep"): return True
        else: return False


    def _cases(self, name):
        if ((name == "mention") or (name == "type_gamma")):
            delta, name = self._mention()
        elif (name == "youtube"): delta = self._youtube()
        elif (name == "type_epsilon") or (name == "reply_type1"): 
            delta, name = self._type1_epsilon_delta()
        else: delta = getattr(self.admin.orm.api.state, f"{name}_delta")
        message, seconds = self._delta(delta)
        return name, message, seconds


    def _store(self, message, name, database):
        if   (name == "type_gamma"): name = "mention"
        elif (name == "type_epsilon"):  name = "reply_type1"
        if database: self.admin.orm.api.messages.create(message, name)
        return message, name


    def _delta(self, delta):
        f           = lambda t: str(t).zfill(2)
        seconds     = (normalize(delta) - datetime.utcnow()).total_seconds()
        mins, secs  = divmod(int(seconds), 60)
        hours, mins = divmod(int(mins),    60)
        days, hours = divmod(int(hours),   24)
        days, hours, mins, secs = f(days), f(hours), f(mins), f(secs)
        data        = f"\u03B4T -{hours}:{mins}:{secs}"
        if (int(days) and (0 <= int(days))):
            data   += f", {days} days"
        if abs(seconds) != seconds:
            data    = "Waiting on controller to initiate exec."
        return data, seconds


    def _efficency(self):
        xQ = self.admin.orm.api.users.count("unfriendQ")
        e = 400 / xQ
        p = round(e * 100, 2)
        return e, p


    def _mention(self):
        hour = datetime.utcnow().hour
        if ((6 <= hour) and (hour <= 16)):
            delta = normalize(self.admin.orm.api.state.type_gamma_delta)
            delta = (delta, "type_gamma")
        else:
            mdelta = normalize(self.admin.orm.api.state.mention_delta)
            gdelta = normalize(self.admin.orm.api.state.type_gamma_delta)
            delta  = min((mdelta, "mention"), (gdelta, "type_gamma"), 
                    key = lambda d: d[0])
        return delta


    def _youtube(self):
        ydelta = normalize(self.admin.orm.api.state.ystream_delta)
        pdelta = normalize(self.admin.orm.api.state.playlist_delta)
        delta  = min(ydelta, pdelta)
        return delta


    def _friend(self, message, seconds):
        if not (abs(seconds) == seconds): return message
        e, p = self._efficency()
        if (1 <= e): return message
        message += f"  (\u03C7Q overload; operating at {p}% efficency.)"
        return message


    def _tweet(self, message, seconds):
        if not (abs(seconds) == seconds): return message
        hour = datetime.utcnow().hour
        if (6 <= hour) and (hour <= 16) and ("asleep" not in message):
            message += "  (TweetMakerAI tweet composer.)"
        return message


    def _scraper_type_epsilon(self, message, seconds):
        if not (abs(seconds) == seconds): return message
        message += f"  (tweet scraper type-\u03B5)"
        return message

    
    def _type1_epsilon_delta(self):
        count = self.admin.orm.api.tweets.count(type = "reply_type1")
        hour  = datetime.utcnow().hour
        if (((6 <= hour) and (hour <= 16)) or (not count)): 
            delta = self.admin.orm.api.state.type_epsilon_subcycle_delta
            name  = "type_epsilon"
        else:
            delta = self.admin.orm.api.state.reply_type1_delta
            name = "reply_type1"
        delta = normalize(delta)
        return delta, name


    def _inactive(self, message, seconds):
        if not (abs(seconds) == seconds): return message
        message += f"  (tweet scraper type-\u03C6)"
        e, p = self._efficency()
        if (1 <= e): return message
        message += f"   \u03C7Q overload;   \u2234  {p}% \u03B5"
        return message

    
    def _type_gamma(self, message, seconds):
        if not (abs(seconds) == seconds): return message
        message += f"  (tweet scraper type-\u0393)"
        return message
