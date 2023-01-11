from model.orm.objects.super.object import SuperObject


class User(SuperObject):


    def __init__(self, admin, id):
        super().__init__(admin)
        self.id = id


    def _getter(self, idx):
        sql = f"SELECT * FROM user WHERE id = {self.id};"
        return super()._getter(sql, idx)


    def _setter(self, p, val):
        sql = f"UPDATE user SET {p} = ? WHERE id = {self.id};"
        super()._setter(sql, val)


    @property
    def name(self): return self._getter(1)


    @name.setter
    def name(self, val): self._setter("name", val)


    @property
    def username(self): return self._getter(2)


    @username.setter
    def username(self, val): self._setter("username", val)
