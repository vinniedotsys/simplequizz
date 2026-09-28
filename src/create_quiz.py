import os
import json
import random

from src.database import *

### Convert image to Base64
### path = str
def image_to_base64(path):
    if not os.path.isfile(path):
        raise Exception(f"Image not found : {path}")
    with open(path, 'rb') as image_file:
        return image_file.read()

def add_questions_to_game(db_path, game_id, questions):
    game = Game(db_path, game_id)
    game.get()

    order_num = [i for i in range(game.question_number, len(questions))]
    random.shuffle(order_num)

    for key in questions:
        question_choice = Choice(db_path)
        question_choice.emoji = questions[key][1]
        question_choice.get_from_emoji()

        new_question = Question(db_path)
        new_question.game = game_id
        new_question.answer = question_choice.id
        new_question.number = order_num.pop()
        new_question.question_image = image_to_base64(key)
        new_question.answer_image = image_to_base64(questions[key][0])
        new_question.insert()

    game.question_number += len(questions)
    game.update()

def create_from_conf(db_path, conf_path):
    if not os.path.isfile(conf_path):
        raise Exception(f"Image not found : {conf_path}")
    with open(conf_path, 'r') as conf:
        conf_dict = json.loads(conf.read())

    new_game = Game(db_path)
    new_game.gamemaster = conf_dict["gamemaster"]
    questions = conf_dict["questions"]
    new_game.insert()

    for choice in conf_dict["choices"]:
        new_choice = Choice(db_path)
        new_choice.game = new_game.id
        new_choice.emoji = choice
        new_choice.insert()

    add_questions_to_game(db_path, new_game.id, questions)
