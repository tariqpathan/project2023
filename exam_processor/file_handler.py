import os
from pathlib import Path
from PIL import Image

BASE_PATH = ''
QUESTION_PATH = ''

#TODO: get file path location and add it in 
#TODO: check if Path objects required or strings

def construct_filepath(filename: str, base_path: str=BASE_PATH) -> Path:
    """Constructs a file path object from a BASE_PATH and a filename"""
    return os.path.join(base_path, filename)

def get_valid_path(file_path: str):
    """Returns a valid path or raises an exception"""
    if not os.path.isfile(file_path):
        raise Exception(f'file not found at {file_path}')
    return os.path(file_path)

def save_image(image: Image.Image, relative_path: str) -> str:
    """Saves an image to a predetermined location and returns filepath"""
    full_path = os.path.join(QUESTION_PATH, relative_path)
    image.save(full_path)
    return full_path
    