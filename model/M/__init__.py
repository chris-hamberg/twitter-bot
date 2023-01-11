from model.M.users.interface import UnfollowInactiveFollowers
from model.M.users.interface import FollowerQManager
from model.M.users.interface import FollowerManager
from model.M.users.interface import ScraperTypeAlpha
from model.M.users.interface import FriendManager

from model.M.engage.mentions.type_gamma.interface import ScraperTypeGamma
from model.M.engage.mentions.interface import MentionsManager
from model.M.engage.tweets.interface import TweetManager
from model.M.engage.reply.type1 import ReplyType1Manager
from model.M.engage.reply.type2 import ReplyType2Manager

from model.M.content.interface import ScraperTypeLambda
from model.M.content.interface import RSSParseManager
from model.M.content.interface import YouTubeManager
from model.M.content.interface import Nergal


class Managers(list):


    def __init__(self, admin):
        self.append(UnfollowInactiveFollowers(admin))
        self.append(FollowerManager(admin, "follower"))
        self.append(FollowerManager(admin, "following"))
        self.append(FollowerQManager(admin))
        self.append(ScraperTypeAlpha(admin))

        self.append(ScraperTypeLambda(admin))
        self.append(YouTubeManager(admin))
        self.append(RSSParseManager(admin))
        self.append(Nergal(admin))

        self.append(FriendManager(admin, "friend"))
        self.append(FriendManager(admin, "unfriend"))

        self.append(ReplyType1Manager(admin))
        self.append(ReplyType2Manager(admin))
        self.append(TweetManager(admin))
        self.append(ScraperTypeGamma(admin))
        self.append(MentionsManager(admin))
