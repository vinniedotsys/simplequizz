import inspect
import sys

from src.database import *


def check_and_exec(function, params):
    current_module = sys.modules[__name__]
    functions_list = [name for name, obj in inspect.getmembers(current_module, inspect.isfunction)]
    
    if function in functions_list:
        func = getattr(current_module, function)
        func(params)
    else:
        print("Valid functions are : ", functions_list)
