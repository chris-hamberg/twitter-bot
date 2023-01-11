from model.orm.objects.super.object import SuperObject
from model.orm.objects.user import User
import traceback
import requests
import logging


log = logging.getLogger(__name__)


class Resource(SuperObject):


    def __init__(self, admin, id):
        super().__init__(admin)
        self._user = User(admin, id)
        self._id   = id


    def _getter(self, idx):
        sql = (f"SELECT * FROM resource "
               f"WHERE admin = {self._admin.id} AND id = {self._id}")
        return super()._getter(sql, idx)


    def _setter(self, p, val):
        sql = (f"UPDATE resource SET {p} = ? "
               f"WHERE admin = {self._admin.id} AND id = {self._id}")
        super()._setter(sql, val)


    @property
    def id(self): return self._getter(1)


    @id.setter
    def id(self, val):
        self._id = val
        self._setter("id", val)


    @property
    def name(self): return self._user.name


    @name.setter
    def name(self, val): self._user.name = val


    @property
    def username(self): return self._user.username


    @username.setter
    def username(self, val): self._user.username = val


    @property
    def complete(self): return self._getter(2)


    @complete.setter
    def complete(self, val): self._setter("complete", val)


    @property
    def pagination(self): return self._getter(3)


    @pagination.setter
    def pagination(self, val):
        try:
            assert isinstance(val, requests.Response)
            val = val.json().get("meta").get("next_token")
        except AttributeError:
            e = traceback.format_exc()
            log.error(f"{self._admin.name}\n{e}")
        except AssertionError: pass
        finally: self._setter("pagination", val)
