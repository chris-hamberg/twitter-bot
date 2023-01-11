from model.orm.api.users.administrators import Administrators
import random


class TextAnimation:


    def __init__(self, db):
        self.admins = Administrators(db)
        self._gfx = [dict() for admin in self.admins]
        self._seq = [
                "˥", "˦", "˧", "˨", "˩", "˨", "˧", "˦", "˥", "˦", "˧", "˨", "˩",
                
                "˨", "˧", "˦", "˥", "˦", "˧", "˨", "˩",

                "▖", "▗", "▝", "▘", "▚", "▙", "▜", "▟", "▞", "▖", "▘",
                
                "▖", "▞", "▟", "▜", "▙", "▚", "▘", "▝", "▗", "▖",

                "˥", "˦", "˧", "˨", "˩", "˨", "˧", "˦", "˥",

                "▖", "▗", "▝", "▘▝", "▚▗", "▙▝", "▜ ▝", "▟▝", "▞", "▖", "▘"]
        self._load()


    def _load(self):
        for e, _ in enumerate(self.admins):
            for p in ["follower", "following", "friend", "unfriend", 
                    "reply_type1", "tweet", "type_alpha", "type_lambda", 
                    "youtube", "quantum", "reply_type2", "blog", "inactive", 
                    "destroyer", "mention"]:
                i = random.randrange(len(self._seq) - 1)
                if i == 0:
                    direction = "down"
                elif (i == (len(self._seq) - 1)):
                    direction = "up"
                else:
                    direction = random.choice(["down", "up"])
                self._gfx[e][p] = {"index": i, "direction": direction}


    def animate(self, e, proc, name):
        self.e    = e
        self.name = name
        self._set_animation_direction()
        self._set_animation_index()
        gfx = self._get_animation_gfx()
        return self._get_animation_pad(gfx, proc)


    def _set_animation_direction(self):
        i          = self._get_index()
        start, end = (i == 0), (i == len(self._seq) - 1)
        if end:     self._set_direction("up")
        elif start: self._set_direction("down")


    def _set_animation_index(self):
        i = self._get_index()
        if  self._get_direction() == "up": i -= 1
        else: i += 1
        self._set_index(i)


    def _get_animation_gfx(self):
        i   = self._get_index()
        gfx = self._seq[i]
        return gfx


    def _get_animation_pad(self, gfx, proc):
        if   len(gfx) == 3: return f"{gfx} {proc}"
        elif len(gfx) == 2: return f"{gfx}  {proc}"
        else:               return f"{gfx}   {proc}"


    def _get_direction(self):
        return self._gfx[self.e][self.name]["direction"]


    def _set_direction(self, val): 
        self._gfx[self.e][self.name]["direction"] = val


    def _get_index(self): return self._gfx[self.e][self.name]["index"]


    def _set_index(self, val): self._gfx[self.e][self.name]["index"] = val
