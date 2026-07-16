import os
import json

from src.database import *

def image_to_base64(path):
    if not os.path.isfile(path):
        raise Exception(f"Image not found : {path}")
    with open(path, 'rb') as image_file:
        return image_file.read()

def create_from_conf(db_path, conf_path):
    if not os.path.isfile(conf_path):
        raise Exception(f"Image not found : {conf_path}")
    with open(conf_path, 'r') as conf:
        conf_dict = json.loads(conf.read())

    new_game = Game(db_path)
    new_game.gamemaster = conf_dict["gamemaster"]
    questions = conf_dict["questions"]
    new_game.question_number = len(questions)
    new_game.insert()

    for key in questions:

