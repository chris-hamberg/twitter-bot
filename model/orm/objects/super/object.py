import traceback
import logging


log = logging.getLogger(__name__)


class SuperObject:


    def __init__(self, admin):
        self._admin = admin


    def _getter(self, sql, idx, message = None):
        try: return self._admin._accessor.execute_read(sql)[0][idx]
        except IndexError: self._error(message, sql)


    def _setter(self,sql,val): self._admin._accessor.execute_commit(sql,(val,))


    def _error(self, error = None, sql = None):
        if not error: error = traceback.format_exc()
        #log.info(f"{self._admin.name}\n{error}")
        #if sql: log.info(f"{self._admin.name}\n{sql}")
