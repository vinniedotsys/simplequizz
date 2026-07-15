import os
import sqlite3
import uuid

from typing import Optional

class DBObject:
    TABLE = ""
    FIELDS = ""

    def __init__(self, db_path, id=str(uuid.uuid7().hex)) -> None:
        self.db_path = db_path
        if len(id) != 32:
            raise ValueError("Not a valid ID")
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

    def get(self, id):
        if len(id) != 32:
            raise ValueError("Not a valid ID")
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        res = cur.execute(f"SELECT * FROM {self.TABLE} WHERE id=?", (id,))
        line = res.fetchone()
        con.close()
        if line is None:
            raise Exception("Record not found")
        i = 0
        for keys in vars(self):
            if keys == "db_path":
                continue
            else:
                setattr(self, keys, line[i])
                i += 1

    def insert(self, *fields):
        diff = len(vars(self)) - len(fields)
        diff -= 2 #always self defined
        if diff != 0:
            raise Exception(f"Missing {diff} fields Table fields : {self.FIELDS}")
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(f"INSERT INTO {self.TABLE} VALUES ('{self.id}', ?)", fields)
        con.commit()
        con.close()
        self.get(self.id)


class Players(DBObject):
    TABLE = "players"
    FIELDS = "(id TEXT PRIMARY KEY, name TEXT)"
    def __init__(self, db_path, id=str(uuid.uuid7().hex)) -> None:
        super().__init__(db_path, id)
        self.name: Optional[str] = None

class Games(DBObject):
    TABLE = "games"
    FIELDS = "(id TEXT PRIMARY KEY, question_number INTEGER, winner TEXT, gamemaster TEXT, FOREIGN KEY(winner,gamemaster) REFERENCES players(id,id))"
    def __init__(self, db_path, id=str(uuid.uuid7().hex)) -> None:
        super().__init__(db_path, id)
        self.question_number: Optional[int] = None

class Questions(DBObject):
    TABLE = "questions"
    FIELDS = "(id TEXT PRIMARY KEY, game TEXT, answer TEXT, question_image BLOB, answer_image BLOB, number INTEGER, FOREIGN KEY(game) REFERENCES games(id), FOREIGN KEY(answer) REFERENCES choices(id))"
    def __init__(self, db_path, id=str(uuid.uuid7().hex)) -> None:
        super().__init__(db_path, id)
        self.game: Optional[str] = None
        self.answer: Optional[str] = None
        self.order: Optional[int] = None
        self.question_image: Optional[bytes] = None
        self.answer_image: Optional[bytes] = None

class Choices(DBObject):
    TABLE = "choices"
    FIELDS = "(id TEXT PRIMARY KEY, emoji TEXT, game TEXT, FOREIGN KEY(game) REFERENCES games(id))"
    def __init__(self, db_path, id=str(uuid.uuid7().hex)) -> None:
        super().__init__(db_path, id)
        self.emoji: Optional[str] = None
        self.question: Optional[str] = None

class PlayerAnswers(DBObject):
    TABLE = "player_answers"
    FIELDS = "(id TEXT PRIMARY KEY, question TEXT, player TEXT, answer TEXT, result INTEGER, FOREIGN KEY(question) REFERENCES questions(id), FOREIGN KEY(player) REFERENCES players(id), FOREIGN KEY(answer) REFERENCES choices(id))"
    def __init__(self, db_path, id=str(uuid.uuid7().hex)) -> None:
        super().__init__(db_path, id)
        self.question: Optional[str] = None
        self.player: Optional[str] = None
        self.anwser: Optional[str] = None
        self.result: Optional[int] = None

