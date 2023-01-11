from model.orm.api.super.accessor import Accessor
import os


class Engine:


    def __init__(self, db):
        self._accessor = Accessor(db = db)

    
    def paths(self):
        p = []
        gamma = lambda f: os.path.join(root, f).count("OLD")
        sigma = lambda f: f.endswith(".swp") or f.endswith(".txt")
        for root, _, files in os.walk("model/orm/entities"):
            for file in files:
                if any((sigma(file), gamma(file))): continue
                p.append(os.path.join(root, file))
        return p


    def create_tables(self):
        for path in self.paths():
            with open(path, "r") as fhand: sql = fhand.read()
            self._accessor.executescript(sql)
