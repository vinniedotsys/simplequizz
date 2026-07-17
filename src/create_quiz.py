import os
import json
import random

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

    choices_ref = {}
    order_num = [i for i in range(new_game.question_number)]
    random.shuffle(order_num)

    for choice in conf_dict["choices"]:
        new_choice = Choice(db_path)
        new_choice.game = new_game.id
        new_choice.emoji = choice
        new_choice.insert()
        choices_ref[choice] = new_choice.id

    for key in questions:
        new_question = Question(db_path)
        new_question.game = new_game.id
        new_question.answer = choices_ref[questions[key][1]]
        new_question.question_image = image_to_base64(key)
        new_question.answer_image = image_to_base64(questions[key][0])
        new_question.order = order_num.pop()
        new_question.insert()
