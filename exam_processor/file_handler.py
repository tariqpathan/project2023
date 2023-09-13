import os
from pathlib import Path

BASE_PATH = ''

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

