from model.orm.api.super.implementation import Implementation
import sqlite3
import time


class Accessor:


    def __init__(self, admin = None, db = None):
        self.implementation = Implementation(admin = admin, db = db)


    def execute_read(self, sql, data = None): 
        return self.implementation.execute_read(sql, data)
                

    def execute_commit(self, sql, data = None):
        while True:
            try: self.implementation.execute_commit(sql, data)
            except sqlite3.OperationalError: time.sleep(1) 
            else: break


    def executemany(self, sql, data):
        while True:
            try: self.implementation.executemany(sql, data)
            except sqlite3.OperationalError: time.sleep(1)
            else: break


    def execute_transaction(self, transaction):
        while True:
            try: self.implementation.execute_transaction(transaction)
            except sqlite3.OperationalError: time.sleep(1)
            else: break


    def executemany_transaction(self, transaction):
        while True:
            try: self.implementation.executemany_transaction(transaction)
            except sqlite3.OperationalError: time.sleep(1)
            else: break


    def executescript(self, sql):
        while True:
            try: self.implementation.executescript(sql)
            except sqlite3.OperationalError: time.sleep(1)
            else: break
