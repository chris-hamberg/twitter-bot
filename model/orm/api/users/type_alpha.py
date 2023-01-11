from datetime import datetime


class ScraperTypeAlpha:


    def __init__(self, admin):
        self._admin = admin


    def create(self, users, priority = 0, resource = None):
        users = self._admin.orm.api.users._create("type_alpha", users, 
                    priority = priority)
        sql   = ("INSERT OR IGNORE INTO type_alpha (admin, id, resource) "
                f"VALUES ({self._admin.id}, ?, ?);")
        ids   = [(u[0], resource) for u in users]
        self._admin._accessor.executemany(sql, ids)
        sql   = ("UPDATE user_s SET priority = 1 "
                f"WHERE admin = {self._admin.id} AND id = ?")
        ids   = [(id[0],) for id in ids]
        self._admin._accessor.executemany(sql, ids)


    def read(self, delta=None, following=None, quantum=None, short=False):
        data, projection = [], "id, name, username" if short else "*"
        sql = (f"SELECT {projection} FROM user "
                "NATURAL JOIN type_alpha NATURAL JOIN user_s "
               f"WHERE admin = {self._admin.id}")
        if delta:
            sql +=  " AND delta <= ?" if not quantum else ""
            sql +=  " AND delta >= ?" if quantum     else ""
            data.append(datetime.utcnow())
        if isinstance(following, bool):
            sql += " AND following = ?"
            data.append(following)
        return self._admin._accessor.execute_read(f"{sql};", data)
        


    def update(self, id, delta, following):
        sql  = ("UPDATE type_alpha SET following = ? "
               f"WHERE admin = {self._admin.id} AND id = ?;")
        self._admin._accessor.execute_commit(sql, (following, id))
        sql  = ("UPDATE user_s SET delta = ? "
               f"WHERE admin = {self._admin.id} AND id = ?;")
        self._admin._accessor.execute_commit(sql, (delta, id))


    def delete(self, users = None, resource = None):
        if users: self._admin.orm.api.users._delete("type_alpha", users)
        else:
            transaction = []
            sql  = (f"SELECT id FROM type_alpha NATURAL JOIN user_c "
                    f"WHERE admin = {self._admin.id}")
            sql += " AND resource = ?;" if resource else ";"
            if not resource: ids = self._admin._accessor.execute_read(sql)
            else: ids = self._admin._accessor.execute_read(sql, (resource,))
            for entity in ("user_c", "type_alpha"):
                sql  = f"DELETE FROM {entity} WHERE admin = {self._admin.id}"
                sql +=  " AND cat = 'type_alpha'" if (entity == "user_c") else ""
                sql +=  " AND id = ?;"
                transaction.append((sql, ids))
            self._admin._accessor.executemany_transaction(transaction)


    def count(self): return self._admin.orm.api.users.count("type_alpha")
