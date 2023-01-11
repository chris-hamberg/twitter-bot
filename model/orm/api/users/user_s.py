from datetime import timedelta
from datetime import datetime


class UserState:


    def __init__(self, admin):
        self._admin = admin


    def update(self, user, ucount):
        sql  = (f"UPDATE user_s SET unfollowed_count = ? WHERE "
                f"admin = {self._admin.id} AND id = ?;")
        data = (ucount, user[0])
        self._admin._accessor.execute_commit(sql, data)


    def inactive_delta(self, user):
        self.update(user, 3)
        sql = (f"UPDATE user_s SET delta = ? WHERE "
               f"admin = {self._admin.id} AND id = ?;")
        delta = datetime.utcnow()
        data  = (delta, user[0])
        self._admin._accessor.execute_commit(sql, data)


    def error(self, user):
        self.update(user, 3)
        sql = (f"UPDATE user_s SET delta = ? WHERE "
               f"admin = {self._admin.id} AND id = ?;")
        delta = datetime.utcnow() - timedelta(weeks = 40)
        data = (delta, user[0])
        self._admin._accessor.execute_commit(sql, data)
