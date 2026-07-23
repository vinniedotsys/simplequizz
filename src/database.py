import os
import sqlite3
import uuid6

from typing import Optional

class DBObject:
    TABLE = ""
    FIELDS = ""

    def __init__(self, db_path, id=None) -> None:
        if id is None:
            id = str(uuid6.uuid7().hex)
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

    def get(self, id=None):
        if id is None:
            id = self.id
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

    def insert(self):
        excluded = {"db_path", "id"}
        data = {k: v for k, v in vars(self).items() if k not in excluded}
     
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())
     
        query = f"INSERT INTO {self.TABLE} (id, {columns}) VALUES (?, {placeholders})"
     
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, (self.id, *values))
        con.commit()
        con.close()
     
        self.get()

    def update(self):
        excluded = {"db_path", "id"}
        data = {k: v for k, v in vars(self).items() if k not in excluded}

        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = tuple(data.values())

        query = f"UPDATE {self.TABLE} SET {set_clause} WHERE id = ?"
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, (*values, self.id))
        con.commit()
        con.close()

        self.get(self.id)


class Player(DBObject):
    TABLE = "players"
    FIELDS = "(id TEXT PRIMARY KEY, name TEXT, discord_id INTEGER)"
    def __init__(self, db_path, id=None) -> None:
        super().__init__(db_path, id)
        self.name: Optional[str] = None
        self.discord_id: Optional[int] = None

    def is_player(self):
        if self.discord_id is None:
            Exception("No valid Discord User ID")
        query = "SELECT name,id FROM players WHERE discord_id = ?"
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        res = cur.execute(query, (self.discord_id,))
        player = res.fetchone()
        con.close()
        if player is None:
            self.insert()
            return
        if self.name != player[0]:
            self.id = player[1]
            self.update()
            return

class Game(DBObject):
    TABLE = "games"
    FIELDS = "(id TEXT PRIMARY KEY, question_number INTEGER, winner TEXT, gamemaster TEXT, FOREIGN KEY(winner,gamemaster) REFERENCES players(id,id))"
    def __init__(self, db_path, id=None) -> None:
        super().__init__(db_path, id)
        self.question_number: Optional[int] = None
        self.winner: Optional[str] = None
        self.gamemaster: Optional[str] = None

    def available(self):
        query = "SELECT id,question_number FROM games WHERE winner = '' AND gamemaster = ?"
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        res = cur.execute(query, (self.gamemaster,))
        games = res.fetchall()
        con.close()
        return games


class Question(DBObject):
    TABLE = "questions"
    FIELDS = "(id TEXT PRIMARY KEY, game TEXT, answer TEXT, question_image BLOB, answer_image BLOB, number INTEGER, FOREIGN KEY(game) REFERENCES games(id), FOREIGN KEY(answer) REFERENCES choices(id))"
    def __init__(self, db_path, id=None) -> None:
        super().__init__(db_path, id)
        self.game: Optional[str] = None
        self.answer: Optional[str] = None
        self.number: Optional[int] = None
        self.question_image: Optional[bytes] = None
        self.answer_image: Optional[bytes] = None

class Choice(DBObject):
    TABLE = "choices"
    FIELDS = "(id TEXT PRIMARY KEY, emoji TEXT, game TEXT, FOREIGN KEY(game) REFERENCES games(id))"
    def __init__(self, db_path, id=None) -> None:
        super().__init__(db_path, id)
        self.emoji: Optional[str] = None
        self.game: Optional[str] = None

class PlayerAnswer(DBObject):
    TABLE = "player_answers"
    FIELDS = "(id TEXT PRIMARY KEY, question TEXT, player TEXT, answer TEXT, result INTEGER, FOREIGN KEY(question) REFERENCES questions(id), FOREIGN KEY(player) REFERENCES players(id), FOREIGN KEY(answer) REFERENCES choices(id))"
    def __init__(self, db_path, id=None) -> None:
        super().__init__(db_path, id)
        self.question: Optional[str] = None
        self.player: Optional[str] = None
        self.anwser: Optional[str] = None
        self.result: Optional[int] = None

