import os
import json

from src.database import *

def image_to_base64(path):
    if not os.path.isfile(path):
        raise Exception(f"Image not found : {path}")
    with open(path, 'rb') as image_file:
        return image_file.read()
