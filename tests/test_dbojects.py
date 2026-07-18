import unittest
import os
import sqlite3

from src.database import *

class DBOTest(unittest.TestCase):

    def test_empty_db(self):
        test_player = Player('data/test.db')
        test_path = os.path.isfile('data/test.db')
        self.assertEqual(test_path, True)

    def test_empty_table(self):
        con = sqlite3.connect("data/test.db")
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchone()
        con.close()
        test_table = "players" in tables
        self.assertEqual(test_table, True)
    
    def test_foreign_key_oncreate(self):
        test_game = Game('data/test.db')
        con = sqlite3.connect("data/test.db") 
        cur = con.cursor()
        res = cur.execute("PRAGMA foreign_key_list('games')")
        foreign_keys = res.fetchall()
        con.close()
        tables = str(foreign_keys[0][3]) + " " + str(foreign_keys[1][3])
        self.assertEqual("winner gamemaster", tables)

    def test_remaing_objects(self):
        test_choice = Choice('data/test.db')
        test_question = Question('data/test.db')
        test_player_answer = PlayerAnswer('data/test.db')
        con = sqlite3.connect('data/test.db')
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = str(res.fetchall())
        con.close()
        self.assertEqual("[('players',), ('games',), ('choices',), ('questions',), ('player_answers',)]", tables)

    def test_insert(self):
        test_player = Player('data/test.db')
        test_player.name = "LouisdeGie"
        test_player.insert()
        con = sqlite3.connect('data/test.db')
        cur = con.cursor()
        res = cur.execute("SELECT name FROM players WHERE name = 'LouisdeGie'")
        test = res.fetchone() is None
        self.assertEqual(test, False)

#    def test_get(self):
#        test_player = Player('data/test.db')
#        test_player.get(self.shared_user)
#        result = {'db_path': 'data/test.db', 'id': '019ed227090c765abc9e2aa2801a6aa1', 'name': 'LouisdeGie'}
#        self.assertEqual(self.shared_user, test_player.id)
