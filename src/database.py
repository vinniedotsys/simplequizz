import os
import sqlite3
import uuid

from typing import Optional

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
    def __init__(self, db_path, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.name: Optional[str] = None

class Games(DBObject):
    TABLE = "games"
    FIELDS = "(id TEXT PRIMARY KEY, question_number INTEGER, winner TEXT, gamemaster TEXT, FOREIGN KEY(winner,gamemaster) REFERENCES players(id,id))"
    def __init__(self, db_path, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.question_number: Optional[int] = None

class Questions(DBObject):
    TABLE = "questions"
    FIELDS = "(id TEXT PRIMARY KEY, game TEXT, answer TEXT, number INTEGER, FOREIGN KEY(game) REFERENCES games(id), FOREIGN KEY(answer) REFERENCES choices(id))"
    def __init__(self, db_path, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.game: Optional[str] = None
        self.answer: Optional[str] = None
        self.order: Optional[int] = None

class Choices(DBObject):
    TABLE = "choices"
    FIELDS = "(id TEXT PRIMARY KEY, emoji TEXT, question TEXT, FOREIGN KEY(question) REFERENCES games(id))"
    def __init__(self, db_path, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.emoji: Optional[str] = None
        self.question: Optional[str] = None

class PlayerAnswers(DBObject):
    TABLE = "player_answers"
    FIELDS = "(id TEXT PRIMARY KEY, question TEXT, player TEXT, answer TEXT, result INTEGER, FOREIGN KEY(question) REFERENCES questions(id), FOREIGN KEY(player) REFERENCES players(id), FOREIGN KEY(answer) REFERENCES choices(id))"
    def __init__(self, db_path, id=uuid.uuid4()) -> None:
        super().__init__(db_path, id)
        self.question: Optional[str] = None
        self.player: Optional[str] = None
        self.anwser: Optional[str] = None
        self.result: Optional[int] = None

