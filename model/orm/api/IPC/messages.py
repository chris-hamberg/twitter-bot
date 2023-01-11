from model.orm.objects.message import Message
from datetime import timedelta
from datetime import datetime


class Messages(list):


    def __init__(self, admin):
        self._admin = admin
        self.get()


    def get(self):
        self.clear()
        for message in self.read(): self.append(Message(self._admin, message[0]))


    def create(self, data, process):
        sql = (f"DELETE FROM message "
               f"WHERE admin = {self._admin.id} AND delta <= ?;")
        delta = datetime.utcnow() - timedelta(minutes = 6) 
        transaction = [(sql, (delta,))]
        sql = (f"INSERT INTO message (admin, admin_name, data, process) "
               f"VALUES ({self._admin.id}, '{self._admin.name}', ?, ?);")
        transaction.append((sql, (data, process)))
        self.delete(process)
        self._admin._accessor.execute_transaction(transaction)
        self.get()


    def read(self):
        sql = f"SELECT * FROM message WHERE admin = {self._admin.id};"
        return self._admin._accessor.execute_read(sql)


    def delete(self, process):
        sql  = (f"DELETE FROM message "
                f"WHERE admin = {self._admin.id} AND process = ?;")
        self._admin._accessor.execute_commit(sql, (process,))


    def count(self): return len(self)
