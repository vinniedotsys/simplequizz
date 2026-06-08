import unittest
import os
import sqlite3

from src.database import *

class DBOTest(unittest.TestCase):
    def test_empty_db(self):
        test_player = Players('data/test.db', 'LouisdeGie')
        test_path = os.path.isfile('data/test.db')
        self.assertEqual(test_path, True)

    def test_empty_table(self):
        con = sqlite3.connect("data/test.db")
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchone()
        test_table = "players" in tables
        self.assertEqual(test_table, True)
