from model.orm.objects.administrator import Administrator
from model.orm.api.super.accessor import Accessor


class Administrators(list):


    def __init__(self, db):
        self._accessor = Accessor(db = db)
        self._db = db
        self.get()


    def get(self):
        self.clear()
        for admin in self.read(): self.append(Administrator(self._db, admin[0]))

    
    def create(self, **auth):
        admin = Administrator(self._db, **auth)
        self.get()


    def read(self):
        sql = "SELECT * FROM user NATURAL JOIN administrator;"
        return self._accessor.execute_read(sql)


    def delete(self, idx):
        admin = self[idx]
        admin._delete()
        self.pop(idx)


    def count(self): return len(self)
