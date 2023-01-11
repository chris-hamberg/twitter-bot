from model.orm.objects.super.administrator import SuperAdministrator
import traceback


class Administrator(SuperAdministrator):


    def __init__(self, db, id = None, **auth):
        super().__init__(db, id, **auth)


    def _getter(self, idx = None):
        sql  = f"SELECT * FROM administrator WHERE id = {self._id};"
        data = self._accessor.execute_read(sql)[0]
        if idx != None: return data[idx]
        else: return data


    def _setter(self, p, val):
        sql = f"UPDATE administrator SET {p} = ? WHERE id = {self._id}"
        self._accessor.execute_commit(sql, (val,))


    @property
    def db(self): return self._db


    @db.setter
    def db(self, val): self._db = val


    @property
    def id(self): return self._getter(0)


    @id.setter
    def id(self, val):
        self._setter("id", val)
        self._id = int(val)
        try: self.orm.api.state.id = val
        except AttributeError:
            e = traceback.format_exc()


    @property
    def name(self):
        sql  = f"SELECT * FROM user WHERE id = {self._id};"
        return self._accessor.execute_read(sql)[0][1]


    @name.setter
    def name(self, val): self._setter("name", val)


    @property
    def username(self):
        sql = f"SELECT * FROM user WHERE id = {self._id};"
        return self._accessor.execute_read(sql)[0][2]


    @username.setter
    def username(self, val): self._setter("username", val)


    @property
    def auth(self): return self._getter(1)


    @auth.setter
    def auth(self, val): self._setter("auth", val)


    @property
    def bearer(self): return self._getter(2)


    @bearer.setter
    def bearer(self, val): self._setter("bearer", val)


    @property
    def youtube_api(self): return self._getter(3)


    @youtube_api.setter
    def youtube_api(self, val): self._setter("youtube_api", val)
