import inspect
import sys

from src.database import *


def check_and_exec(function, *params):
    current_module = sys.modules[__name__]
    functions_list = [name for name, obj in inspect.getmembers(current_module, inspect.isfunction)]
    
    if function in functions_list:
        func = getattr(current_module, function)
        func(params)
    else:
        print("Valid functions are : ", functions_list)


def clear_results(db_path, game_id):
    game = Game(db_path=db_path, id=game_id)
    answsers = game.answers()
    for answer in answsers:
        to_delete  = PlayerAnswer(db_path=db_path, id=answer)
        to_delete.delete()
