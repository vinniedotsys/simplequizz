import os
import sqlite3
import uuid

class DBObject:
    TABLE = ""
    FIELDS = ()

    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.check_db()
        self.check_table()

    def check_db(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.isfile(self.db_path):
            with open(self.db_path, 'w') as f:
                return
    def check_table(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        res = cur.execute(f"SELECT name FROM sqlite_master WHERE name='{self.TABLE}'")
        if res.fetchone() is None:
            cur.execute(f"CREATE TABLE {self.TABLE}{self.FIELDS}")

class Players(DBObject):
    TABLE = "players"
    FIELDS = ("id","name")
    def __init__(self, db_path, name) -> None:
        super().__init__(db_path)
        self.id = uuid.uuid4()
        self.name = name
