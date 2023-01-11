import traceback
import logging
import sqlite3
import time


log = logging.getLogger(__name__)


class Implementation:


    def __init__(self, admin = None, db = None):
        self._admin = admin
        self._db    = db


    def _connection(self):
        if isinstance(self._db, sqlite3.Connection): return self._db
        elif hasattr(self._admin, "db"):
            if isinstance(self._admin.db, sqlite3.Connection): 
                return self._admin.db
        return sqlite3.connect(self._db or self._admin.db)


    def _close(self, connection):
        if not isinstance(connection, sqlite3.Connection): 
            connection.close()


    def execute_read(self, sql, data = None):
        connection = self._connection()
        cursor     = connection.cursor()
        result     = None
        while True:
            try:
                if data: q = cursor.execute(sql, data)
                else:    q = cursor.execute(sql)
                result     = q.fetchall()
            except sqlite3.OperationalError:
                time.sleep(1)
                continue
            else:
                self._close(connection)
                return result
                

    def execute_commit(self, sql, data = None):
        connection = self._connection()
        cursor = connection.cursor()
        try:
            if data: cursor.execute(sql, data)
            else: cursor.execute(sql)
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            e = traceback.format_exc()
            log.debug(e)
        finally: self._close(connection)


    def executemany(self, sql, data):
        connection = self._connection()
        cursor     = connection.cursor()
        try:
            cursor.executemany(sql, data)
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            e = traceback.format_exc()
            log.debug(e)
        finally: self._close(connection)


    def execute_transaction(self, transaction):
        connection = self._connection()
        connection.isolation_level = None                            
        cursor = connection.cursor()
        cursor.execute("begin")
        try:
            for trans in transaction:
                if isinstance(trans, tuple):
                    sql, data = trans
                    cursor.execute(sql, data)
                else: cursor.execute(trans)
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            e = traceback.format_exc()
            log.debug(e)
        finally: self._close(connection)


    def executemany_transaction(self, transaction):
        connection = self._connection()
        connection.isolation_level = None
        cursor = connection.cursor()
        cursor.execute("begin")
        try:
            for trans in transaction:
                sql, data = trans
                cursor.executemany(sql, data)
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            e = traceback.format_exc()
            log.debug(e)
        finally: self._close(connection)


    def executescript(self, sql):
        connection = self._connection()
        cursor = connection.cursor()
        try:
            cursor.executescript(sql)
            connection.commit()
        except sqlite3.OperationalError:
            connection.rollback()
            error = traceback.format_exc()
            log.debug(error)
        finally: self._close(connection)
