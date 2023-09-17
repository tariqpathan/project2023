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

def get_valid_image(file_path: str) -> Image.Image:
    """Returns a valid image or raises an exception"""
    image = get_image(file_path)
    if image is None:
        raise Exception(f'invalid image at {file_path}')
    return image

def get_image(file_path: str) -> Image.Image:
    """Returns an image object from a file path"""
    return Image.open(file_path)

def save_image(image: Image.Image, name: str) -> str:
    """Saves an image to a predetermined location and returns filepath"""
    filepath = os.path.join(QUESTION_PATH, name)
    image.save(filepath)
    return filepath

def get_image_filepath(filename: str) -> str:
    """Returns a file path for an image"""
    return os.path.join(QUESTION_PATH, filename)
    