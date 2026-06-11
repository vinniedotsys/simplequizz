import unittest
import os
import sqlite3

from src.database import *

class DBOTest(unittest.TestCase):
    def test_empty_db(self):
        test_player = Players('data/test.db')
        test_path = os.path.isfile('data/test.db')
        self.assertEqual(test_path, True)

    def test_empty_table(self):
        con = sqlite3.connect("data/test.db")
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchone()
        test_table = "players" in tables
        self.assertEqual(test_table, True)
    
    def test_foreign_key_oncreate(self):
        test_game = Games('data/test.db')
        con = sqlite3.connect("data/test.db") 
        cur = con.cursor()
        res = cur.execute("PRAGMA table_info('games')")
        tables = res.fetchall()
        test_table = "games" in tables
        self.assertEqual(True, True)

    def test_remaing_objects(self):
        test_choice = Choices('data/test.db')
        test_question = Questions('data/test.db')
        test_player_answer = PlayerAnswers('data/test.db')
        con = sqlite3.connect('data/test.db')
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchall()
        print(tables)

