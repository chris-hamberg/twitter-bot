from model.M.super.superclass import SuperManager
from model.blog.feed_parser import Blog
from datetime import timedelta
from datetime import datetime
import random


class RSSParseManager(SuperManager):


    def __init__(self, admin):
        self.feeds = Blog(admin)
        self.admin = admin
        self.name  = "blog"


    def execute(self):
        index = self.feeds.parse()
        self.admin.orm.api.state.blog_index = index + 1
        ts = datetime.utcnow() + timedelta(minutes = random.randint(55, 90))
        self.admin.orm.api.state.blog_delta = ts
        self.report("RSS feeds updated.")
