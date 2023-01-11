from model.objects.normalize import normalize
import os


class Parser:


    def __init__(self, admin):
        self.admin = admin


    def parse_conversation(self, text, c_id):
        params, dialog = {"conversation_id": c_id}, []
        conversation   = self.admin.orm.api.tweets.read(**params)
        text           = self._clean(text)
        if not conversation: return [text]
        conversation.sort(key = lambda c: normalize(c[10]))
        for tweet in conversation: dialog.append(self._clean(tweet[1]))
        if (not (text in dialog)): dialog.append(text)
        dialog.reverse()
        return dialog


    def parse_iq(self, field):
        path = ["tweets", f"{self.admin.username}", f"ai_{field}.txt"]
        path = os.path.join(*path)
        with open(path, "r") as fhand: return fhand.read()


    def _clean(self, text):
        text, total, count = text.replace("\n", " #### "), text.count("@"), 0
        text = text.split(" ")
        for e, word in enumerate(text):
            if  (count == total): break
            elif word.count("@"): 
                count  += 1
                text[e] = ""
        text = " ".join(text)
        text = text.replace(" #### ", "\n")
        text = text.strip()
        return text
