from model.objects.exceptions import ForbiddenException
from model.orm.objects.resource import Resource


class Resources(list):


    def __init__(self, admin):
        self._admin = admin
        self.get()


    def get(self):
        self.clear()
        sql  = ("SELECT * FROM user NATURAL JOIN resource "
               f"WHERE admin = {self._admin.id} AND complete = FALSE;")
        for resource in self._admin._accessor.execute_read(sql):
            self.append(Resource(self._admin, resource[0]))


    def create(self, username):
        try:
            r = self._admin.twitter.api(self, self._admin, 
                    **{"username": username, "auth": self._admin.auth})
            id = r.json().get("data").get("id")
            self._admin.orm.api.users._create("resource", r, state = False)
            sql  = ("INSERT OR IGNORE INTO resource (admin, id) "
                   f"VALUES ({self._admin.id}, ?);")
            self._admin._accessor.execute_commit(sql, (id,))
        except ForbiddenException: pass
        self.get()


    def read(self):
        return self._admin.orm.api.users._read("resource", state = False)


    def delete(self, i = None):
        if (i != None):
            users = (self[i].id, self[i].name, self[i].username)
            self._admin.orm.api.type_alpha.delete(resource = users[0])
            self._admin.orm.api.users._delete("resource", users)
        else:
            sql   = ("SELECT * FROM user NATURAL JOIN resource "
                    f"WHERE admin = {self._admin.id} AND complete = TRUE;")
            users = [(u[0], u[1], u[2]) for u in 
                    self._admin._accessor.execute_read(sql)]
            self._admin.orm.api.type_alpha.delete(users)
            self._admin.orm.api.users._delete("resource", users)
        self.get()


    def count(self): return len(self)
