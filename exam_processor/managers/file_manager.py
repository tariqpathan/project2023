import os
from PIL import Image
from typing import Optional


import os

class FileManager:
    
    @staticmethod
    def get_root_path():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def construct_path(filename: str, base_path: Optional[str]=None):
        """Constructs the full path for a given filename."""
        if not base_path:
            base_path = FileManager.get_root_path()
        return os.path.join(base_path, filename)

    @staticmethod
    def is_valid_file(filepath: str) -> bool:
        """Check if the provided path exists and is a file.
        Args:
            filepath (str): The path to check.

        Returns:
            bool: True if the filepath exists and is a file, otherwise False.
        """
        return os.path.exists(filepath) and os.path.isfile(filepath)

    @staticmethod
    def resolve_path(filename: str, env_var: str) -> str:
        default_path = FileManager.construct_path(filename)
        return os.environ.get(env_var, default_path)


class ImageFileManager:

    @staticmethod
    def get_image_save_path(filename: str) -> str:
        """Returns the path where the image should be saved."""
        #TODO: avoid hardcoding the path
        base_path = FileManager.construct_path("static/question_images")
        return FileManager.construct_path(filename, base_path)

    @staticmethod
    def save_image(image_data, filename: str):
        """Saves the given image data to the specified filename in the image directory."""
        save_path = ImageFileManager.get_image_save_path(filename)
        
        try:
            with open(save_path, 'wb') as image_file:
                image_file.write(image_data)
        except Exception as e:
            raise IOError(f"Unable to save image: {e}")
    
    #TODO: ensure image retrieval works
    @staticmethod
    def get_image(filename: str):
        """Returns the image data for the specified filename."""
        image_path = ImageFileManager.get_image_save_path(filename)
        try:
            with open(image_path, 'rb') as image_file:
                return image_file.read()
        except FileNotFoundError:
            raise ValueError(f"Image file {image_path} not found.")
        except Exception as e:
            raise IOError(f"Unable to read image: {e}")
