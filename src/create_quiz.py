import os
import json
import base64

from src.database import *

def image_to_base64(path):
    if not os.path.isfile(path):
        raise Exception(f"Image not found : {path}")
