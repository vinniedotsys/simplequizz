import unittest

from src.create_quiz import create_from_conf

class CreateTest(unittest.TestCase):
    def test_import_conf(self):
        create_from_conf("data/test.db","build/game.json")
