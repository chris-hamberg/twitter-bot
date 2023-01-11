from model.orm.api.super.accessor import Accessor
from model.orm.api.state.state import State
from model.orm.api.interface import ORM
from model.orm.engine import Engine
from unittest import TestCase
import sqlite3


class Administrator(TestCase):


    def __init__(self, db):
        super().__init__()
        self.setUp()


    def setUp(self):
        self._db = self.db = sqlite3.connect(":memory:")
        engine   = Engine(self.db)
        engine.create_tables()

        self.id = self._id = 12345
        self.name          = "offline admin"
        self.orm           = ORM(self, self.db)
        self._accessor     = Accessor(db = self.db)

        cursor = self.db.cursor()
        sql = (f"INSERT INTO user (id, name, username) "
               f"VALUES ({self.id}, '{self.name}', '{self.name}');")
        cursor.execute(sql)
        sql = (f"INSERT INTO administrator (id) VALUES ({self.id});")
        cursor.execute(sql)
        sql = (f"INSERT INTO user_c (admin, cat, id) "
               f"VALUES ({self.id}, 'admin', {self.id});")
        cursor.execute(sql)
        self.db.commit()

        self.orm.api.state = State(self)
        self.orm.api._init()


    def tearDown(self): self.db.close()
