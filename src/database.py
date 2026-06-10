import os
import sqlite3
import uuid

class DBObject:
    TABLE = ""
    FIELDS = ""

    def __init__(self, db_path, id=uuid.uuid4()) -> None:
        self.db_path = db_path
        self.id = id
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
        con.close()

class Players(DBObject):
    TABLE = "players"
    FIELDS = "(id TEXT PRIMARY KEY, name TEXT)"
    def __init__(self, db_path, name, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.name = name

class Games(DBObject):
    TABLE = "games"
    FIELDS = "(id TEXT PRIMARY KEY, question_number INTEGER, winner TEXT, gamemaster TEXT, FOREIGN KEY(winner,gamemaster) REFERENCES player(id,id))"
    def __init__(self, db_path, question_number=0, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.question_number = question_number
