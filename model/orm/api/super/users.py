from model.orm.api.super.accessor import Accessor
from model.orm.api.users.user_s import UserState
import requests


class SuperUsers:


    def __init__(self, admin = None, db = None):
        self._admin = admin
        if not admin: self._accessor = Accessor(db = db)
        else:
            self._accessor = Accessor(  admin)
            self.state = UserState(admin)


    def create(self, category, users, state, id, priority):
        raise NotImplemented


    def read(self,category,id,state,priority,unfollowed_count,delta,short):
        raise NotImplemented


    def delete(self, category, users):
        raise NotImplemented


    def hard_delete(self, category, users):
        raise NotImplemented


    def count(self, category):
        raise NotImplemented


    def _create(self, category, users, state = True, id = None, priority = 0):
        users       = self._typeset(users)
        transaction = self._create_user(users)
        sql, ids    = self._create_user_c(category, users, id)
        transaction = self._create_user_s(ids, transaction, state, priority)
        self._accessor.executemany_transaction(transaction)                                                                    
        self._accessor.executemany(sql, ids)
        return users


    def _typeset(self, users):
        if isinstance(users, tuple): users = [users]
        elif isinstance(users, requests.Response):
            phi = lambda user: (user["id"], user["name"], user["username"])
            if not users.json().get("includes") and not users.json().get("data"): 
                return []
            elif users.json().get("includes"):
                users = users.json().get("includes").get("users")
            else: users = users.json().get("data")
            if isinstance(users, list):   users = [phi(user) for user in users]
            elif isinstance(users, dict): users = [phi(users)]
        return [(user[0], user[1], user[2]) for user in users]


    def _create_user(self, users):
        return [((f"INSERT OR IGNORE INTO user (id, name, username) "
                   "VALUES (?, ?, ?);"), users)]


    def _create_user_c(self, category, users, id):
        sql = "INSERT OR IGNORE INTO user_c (admin, cat, id) "
        if self._admin: sql += f"VALUES ({self._admin.id}, '{category}', ?);"
        elif id: sql += f"VALUES ({id}, '{category}', ?);"
        ids = [(user[0],) for user in users]
        return sql, ids

    
    def _create_user_s(self, ids, transaction, state, priority):
        if (state and priority):
            ids = [(i[0], priority) for i in ids]
            sql = ("INSERT OR IGNORE INTO user_s (admin, id, priority) "
                  f"VALUES ({self._admin.id}, ?, ?);")
            transaction.append((sql, ids))
        elif state:
            sql = ("INSERT OR IGNORE INTO user_s (admin, id) "
                  f"VALUES ({self._admin.id}, ?);")
            transaction.append((sql, ids))
        return transaction


    def _read(self, category, id = None, state = True, priority = None, 
                unfollowed_count = None, delta = None, short = False):
        data, projection = [category], "id, name, username" if short else "*"
        sql = f"SELECT {projection} FROM user NATURAL JOIN user_c"
        if (state and (category != "resource") and (category != "admin")):
            sql += " NATURAL JOIN user_s"
        elif (category == "resource"): sql += " NATURAL JOIN resource"
        elif    (category == "admin"): sql += " NATURAL JOIN administrator"
        sql += f" WHERE admin = {self._admin.id} AND cat = ?"
        if (state and (category != "resource") and (category != "admin")): 
            if (priority != None): data.append(priority)
            if (delta != None):    data.append(delta)
            sql += " AND priority = ?"          if (priority != None) else ""
            sql += " AND delta <= ?"            if (delta != None)    else ""
            sql += " AND unfollowed_count >= 3" if (unfollowed_count != None
                    ) else ""
        sql += " AND id = ?" if id else ""
        if id: data.append(id)
        return self._accessor.execute_read(f"{sql};", data)


    def _orphans(self):
        sql = "SELECT id FROM user EXCEPT SELECT id FROM user_c;"
        ids = self._accessor.execute_read(sql)
        transaction = []
        sql = f'DELETE FROM user_s WHERE id = ?;'
        transaction.append((sql, ids))
        sql = f'DELETE FROM user WHERE id = ?'
        transaction.append((sql, ids))
        self._accessor.executemany_transaction(transaction)
        return ids


    def _delete(self, category, users = None):
        if isinstance(users, set) and (len(users) == 0): 
            return False
        elif isinstance(users, list) and (len(users) == 0):
            return False
        elif (users != None): 
            if isinstance(users, tuple): users = [users]
            ids = [(user[0],) for user in users]
            transaction = self._delete_transaction_builder(category, ids)
            if (len(transaction[0]) == 1): return False
            self._accessor.executemany_transaction(transaction)
        else:
            transaction = self._delete_transaction_builder(category)
            self._accessor.execute_transaction(transaction)


    def _delete_transaction_builder(self, category, ids = None):

        sigma = lambda q, i: f"{q} AND id = ?;" if i else f"{q};"

        def epsilon(q, i, t):
            if i:  t.append((q, i)) 
            else:  t.append(q)
            return t

        transaction = []
        sql  = (f"DELETE FROM user_c WHERE admin = {self._admin.id} "
                f"AND cat = '{category}'")
        sql = sigma(sql, ids); transaction = epsilon(sql, ids, transaction)

        if (category == "resource") or (category == "type_alpha"):
            sql = f"DELETE FROM {category} WHERE admin = {self._admin.id}"
            sql = sigma(sql, ids); transaction = epsilon(sql, ids, transaction)

        return transaction
