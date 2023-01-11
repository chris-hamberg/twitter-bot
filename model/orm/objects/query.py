from model.orm.objects.super.object import SuperObject
import traceback
import requests


class Query(SuperObject):


    def __init__(self, admin, rowid):
        super().__init__(admin)
        self._rowid = rowid


    def _getter(self, idx):
        sql = f"SELECT * FROM query WHERE rowid = {self._rowid};"
        return super()._getter(sql, idx)


    def _setter(self, p, val):
        sql  = f"UPDATE query SET {p} = ? WHERE rowid = {self._rowid}"
        super()._setter(sql, val)


    @property
    def rowid(self): return self._rowid


    @property
    def q(self): return self._getter(2)


    @q.setter
    def q(self, val): self._setter("q", val)


    @property
    def type(self): return self._getter(3)


    @property
    def pagination(self): return self._getter(4)


    @pagination.setter
    def pagination(self, val):
        try:
            assert isinstance(val, requests.Response)
            val = val.json().get("meta").get("next_token")
        except AttributeError:
            val = None
        except AssertionError: pass
        finally: self._setter("pagination", val)


    @property
    def polling(self): return self._getter(5)


    @polling.setter
    def polling(self, val): self._setter("polling", val)
