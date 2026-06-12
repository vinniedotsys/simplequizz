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
        res = cur.execute("PRAGMA foreign_key_list('games')")
        foreign_keys = res.fetchall()
        tables = str(foreign_keys[0][3]) + " " + str(foreign_keys[1][3])
        self.assertEqual("winner gamemaster", tables)

    def test_remaing_objects(self):
        test_choice = Choices('data/test.db')
        test_question = Questions('data/test.db')
        test_player_answer = PlayerAnswers('data/test.db')
        con = sqlite3.connect('data/test.db')
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = str(res.fetchall())
        self.assertEqual("[('players',), ('games',), ('choices',), ('questions',), ('player_answers',)]", tables)
