class ConversationProcessor:


    def __init__(self, admin):
        self.admin = admin


    def proc(self, conversations, sentinel):
        tweets, hcount = [], 0
        for conversation in conversations:
            dialog   = conversation.dialog
            username = conversation.username
            tweet    = dialog[-1]
            if sentinel(tweet, username): continue
            tweets.append(tweet)
            if len(dialog) <= 1:          continue
            history = dialog[-2]
            self.admin.orm.api.tweets.create([history])
            self.admin.orm.api.tweets.update(history[0])
            hcount += 1
        return tweets, hcount
