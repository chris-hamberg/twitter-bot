from model.orm.objects.query import Query
import traceback
import logging


log = logging.getLogger(__name__)


class Queries(list):


    def __init__(self, admin):
        self._admin = admin
        self.get()


    def get(self):
        self.clear()
        for query in self.read(): self.append(Query(self._admin, query[0]))


    def create(self, query, t):
        sql = ("INSERT OR IGNORE INTO query (admin, query, type) "
              f"VALUES ({self._admin.id}, ?, ?);")
        self._admin._accessor.execute_commit(sql, (query, t))
        self.get()


    def read(self):
        sql = f"SELECT * FROM query WHERE admin = {self._admin.id};"
        return self._admin._accessor.execute_read(sql)


    def delete(self, idx):
        try: rowid = self[idx].rowid
        except IndexError:
            e = traceback.format_exc()
            log.debug(f"{self._admin.name}\n{e}")
            return False
        else:
            sql = f"DELETE FROM query WHERE rowid = {rowid};"
            self._admin._accessor.execute_commit(sql)
            self.pop(idx)


    def count(self): return len(self)
