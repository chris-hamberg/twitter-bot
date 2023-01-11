import random


class Youtube:


    def __init__(self, admin, emojis = None, p = None):
        self.admin = admin
        self.emojis = emojis or str()
        self._probability = p or 0.33


    def set_emojis(self, emojis):
        self.emojis = emojis


    def format_emojis(self):
        if random.random() < self._probability:
            return str()
        e = random.choice(self.emojis.split(","))
        length = random.randint(1, 4)
        emojis = e * length
        return emojis
