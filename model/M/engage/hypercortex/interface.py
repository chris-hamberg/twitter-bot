from model.M.engage.hypercortex.parser import Parser
from model.M.engage.hypercortex.core import Core
from model.M.engage.hypercortex.post import Post


class HyperCortexTypeAlpha:


    def __init__(self, admin, name = None):
        self.core   = Core(admin, name)
        self.post   = Post(admin, name)
        self.parser = Parser(admin)
        self.admin  = admin
        self.kwgs   = dict()


    def state(self, tweet, c_id = None):
        c_id, t_id, text, uid = c_id or tweet[0], tweet[0], tweet[1], tweet[2]
        user = self.admin.orm.api.tweets.user(id = uid, tweet_id = t_id)
        try:               uname = user[0][2]
        except IndexError: uname = "'Unknown'"
        self.kwgs.update({"c_id":c_id, "t_id":t_id, "text":text, "uname":uname})

    
    def compose(self):
        text, c_id    = self.kwgs.get("text"), self.kwgs.get("c_id")
        dialog        = self.parser.parse_conversation(text, c_id)
        ptweet        = dialog[0]
        knowledge     = self.parser.parse_iq("knowledge")
        instruction   = self.parser.parse_iq("instruction")
        self.kwgs.update({"knowledge": knowledge, "instruction": instruction})
        self.kwgs.update({"dialog": dialog, "ptweet": ptweet})
        self.response = self.core.compose(**self.kwgs)
        return self.response


    def send(self):
        c_id, t_id = self.kwgs.get("c_id"), self.kwgs.get("t_id")
        self.post.send(c_id, t_id, self.response)
