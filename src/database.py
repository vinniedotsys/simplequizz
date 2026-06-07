import os
import sqlite3

class DBObject:
    def __init__(self, name, db_path) -> None:
        self.name = name
        self.db_path = db_path
        self.check_db()

    def check_db(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.isfile(self.db_path):
            with open(self.db_path, 'w') as f:
                return

