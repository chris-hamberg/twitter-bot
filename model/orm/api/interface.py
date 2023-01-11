from model.orm.api.users.type_alpha import ScraperTypeAlpha
from model.orm.api.users.resources import Resources
from model.orm.api.users.users import Users

from model.orm.api.content.youtube import YouTube
from model.orm.api.content.blog import Blog

from model.orm.api.tweets.queries import Queries
from model.orm.api.tweets.tweets import Tweets

from model.orm.api.IPC.messages import Messages


class ORM:


    def __init__(self, admin = None, db = None):
        self.api = API(admin, db)



class API:


    def __init__(self, admin = None, db = None):
        self._admin = admin
        self.users  = Users(db = db)


    def _init(self):
        self.users       = Users(           self._admin)
        self.messages    = Messages(        self._admin)
        self.queries     = Queries(         self._admin)
        self.resources   = Resources(       self._admin)
        self.type_alpha  = ScraperTypeAlpha(self._admin)
        self.tweets      = Tweets(          self._admin)
        self.youtube     = YouTube(         self._admin)
        self.blog        = Blog(            self._admin)
