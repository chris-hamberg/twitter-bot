from model.objects.exceptions import ConfigurateXType1Ex
from model.objects.exceptions import ConfigurateXType2Ex
from model.objects.exceptions import ConfigurateXType3Ex
from model.objects.exceptions import StatusCodeException
from model.objects.exceptions import SentinelException
from model.objects.exceptions import NullValue

from model.M.engage.tweets.objects.interface import *

from model.M.super.superclass import SuperManager

from collections import OrderedDict
from datetime import timedelta
from datetime import datetime
import random
import time


class TweetManager(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.name  = "tweet"
        self.type  = OrderedDict({
                "playlist": Playlist, "stream": Ystream, "tweetAI": tweetAI,
                "static"  : Static,   "meme"  : Meme,    "blog"   : Blog})


    def execute(self):
        if self._sentinel_typeAlpha(): return False
        r, t = None, None; self._sentinel_typeOmega(); self._sentinel_typeZeta()
        (Π, Γ), Λ, Δ = self._probability_selectio(), list(self.type.values()), 3
        while all([Π, Γ, Λ, Δ]) and (not t):
            try: r, t = Γ.execute(); t, (Π, Γ), Λ = self._tAI_inject(t, Π, Γ, Λ)
            except ConfigurateXType1Ex: (Π, Γ), Λ = self._conf_type1_ex(Π, Γ, Λ)
            except ConfigurateXType2Ex: (Π, Γ), Λ = self._conf_type2_ex(Π, Γ, Λ)
            except ConfigurateXType3Ex: (Π, Γ), Λ = self._conf_type3_ex(Π, Γ, Λ)
            except StatusCodeException:         Δ = self._stat_codeX_ex(Π, Γ, Δ)
            except NullValue:           (Π, Γ), Λ = self._null_value_ex(Π, Γ, Λ)
            else: break


    def _tAI_inject(self, signal, Π, Γ, Λ):
        if (signal != "Λ"): return signal, (Π, Γ), Λ
        else: Λ.remove(Π);  return None, self._choice(Λ), Λ


    def _conf_type1_ex(self, Π, Γ, Λ):
        self.admin.orm.api.state.tweetAI_subcycle_index = 0
        self.report("tweetAI configuration error.")
        Λ.remove(Π); return self._choice(Λ), Λ


    def _conf_type2_ex(self, Π, Γ, Λ):
        self.report("Blog content is empty or no URL has been provided.")
        Λ.remove(Π); return self._choice(Λ), Λ


    def _conf_type3_ex(self, Π, Γ, Λ):
        self.report(f"{Γ.__class__.__name__} tweet content not configured.")
        Λ.remove(Π); return self._choice(Λ), Λ


    def _stat_codeX_ex(self, Π, Γ, Δ):
        self.report(f"{Γ.__class__.__name__} connection error. Sleep 30 secs.")
        time.sleep(30)
        return Δ - 1


    def _null_value_ex(self, Π, Γ, Λ):
        Λ.remove(Π); Π, X = self._choice(Λ)
        gamma = f"{Γ.__class__.__name__}"
        name  = f"{X.__class__.__name__}"
        if (name == "int"): self.report("Operation failed.")
        else: self.report(f"NULL {gamma} tweet; set {name} ≡ Γ tweet type.")
        return (Π, X), Λ


    def _choice(self, Λ):
        try: Π = random.choice(Λ); Γ = Π(self.admin); return Π, Γ
        except IndexError: return 0, 0


    def _sentinel_typeAlpha(self):
        if self.admin.orm.api.state.tweetAI_subcycle_index: return False
        ρ = round(random.random() * 100, 2)
        if (ρ <= 20): return False
        self.report("20% probability to tweet not met.")
        φ = random.randint(1, 25)
        Δ = datetime.utcnow() + timedelta(minutes = φ)
        self.admin.orm.api.state.tweet_delta = Δ
        return True


    def _sentinel_typeOmega(self):
        Ω = [self.admin.orm.api.state.reply_count,
             self.admin.orm.api.state.retweet_reply_count,
             self.admin.orm.api.state.like_subcycle_count]
        if all(Ω): return False
        Δ       = timedelta(minutes = random.randint(3, 10))
        message = "Sentinel type-Omega: must first reply, retweet, & like."
        self._sentinel_type_generic(message, Δ)


    def _sentinel_typeZeta(self):
        if self.admin.orm.api.state.reply_count < 15: return False
        message = "Sentinel type-Zeta: engagement resting until tomorrow."
        Δ = timedelta(hours = 1); self._sentinel_type_generic(message, Δ)


    def _sentinel_type_generic(self, message, Δ):
        self.admin.orm.api.state.tweet_delta = datetime.utcnow() + Δ
        self.report(message); raise SentinelException


    def _probability_selectio(self):
        Γ  =  Π  =  random.choice(list(self.type.values())[1:-1])
        p        =  int(random.random() * 100)
        if not self.admin.orm.api.state.tweetAI_injection_state:
            if self.admin.orm.api.state.tweetAI_subcycle_index:
                Γ = Π = self.type["tweetAI"]
        elif (p <= 25): Γ = Π = self.type["blog"]
        elif (90 <= p): Γ = Π = self.type["playlist"]
        return Π, Γ(self.admin)
