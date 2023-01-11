from model.orm.objects.super.object import SuperObject


class Message(SuperObject):


    def __init__(self, admin, rowid):
        super().__init__(admin)
        self._rowid = rowid


    def _getter(self, idx):
        sql = (f"SELECT * FROM message WHERE admin = {self._admin.id} "
               f"AND rowid = {self._rowid};")
        msg = (f"{self._admin.name}\n"
               f"Message {self._rowid} no longer exists.")
        return super()._getter(sql, idx, msg)


    def _setter(self, p, val):
        sql  = (f"UPDATE message SET {p} = ? "
                f"WHERE admin = {self._admin.id} AND rowid = {self._rowid};")
        super()._setter(sql, val)


    @property
    def rowid(self): return self._rowid


    @property
    def admin_name(self): return self._getter(2)


    @admin_name.setter
    def admin_name(self, val): self._setter("admin_name", val)


    @property
    def data(self): return self._getter(3)


    @data.setter
    def data(self, val): self._setter("data", val)


    @property
    def process(self): return self._getter(4)


    @process.setter
    def process(self, val): self._setter("process", val)


    @property
    def delta(self): return self._getter(5)
