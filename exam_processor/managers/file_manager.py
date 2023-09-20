import os
from PIL import Image
from typing import Optional


class FileManager:

    BASE_PATH = os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def construct_path(filename: str) -> str:
        """Returns the full path to the provided filename."""
        return os.path.join(FileManager.BASE_PATH, filename)

    @staticmethod
    def is_valid_file(filepath: str) -> bool:
        """Returns True if the provided filepath exists and is a file."""
        return os.path.exists(filepath) and os.path.isfile(filepath)

    @staticmethod
    def resolve_path(filename: str, env_var: str) -> str:
        default_path = FileManager.construct_path(filename)
        return os.environ.get(env_var, default_path)



class ImageFileManager:

    @staticmethod
    def load_image(filepath: str) -> Optional[Image.Image]:
        if FileManager.is_valid_file(filepath):
            try:
                return Image.open(filepath)
            except Exception as e:
                print(f"Failed to load image. Reason: {str(e)}")
                return None
        else:
            return None

    @staticmethod
    def store_image(image: Image.Image, filepath: str) -> bool:
        try:
            image.save(filepath)
            return True
        except Exception as e:
            # Handle error (e.g., print error message, raise exception, etc.)
            print(f"Failed to save image. Reason: {str(e)}")
            return False
