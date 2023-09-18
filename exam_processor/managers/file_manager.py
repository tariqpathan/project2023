import os
from PIL import Image
from typing import Optional

class FileHandler:

    DEFAULT_BASE_PATH = "/path/to/default/base"

    @staticmethod
    def construct_path(filename: str, base_path: Optional[str] = None) -> str:
        """Returns the full path to the provided filename, given the base path."""
        base_path = base_path or FileHandler.DEFAULT_BASE_PATH
        return os.path.join(base_path, filename)

    @staticmethod
    def is_valid_file(filepath: str) -> bool:
        """Returns True if the provided filepath exists and is a file."""
        return os.path.exists(filepath) and os.path.isfile(filepath)


class ImageFileManager:

    @staticmethod
    def load_image(filepath: str) -> Optional[Image.Image]:
        if FileHandler.is_valid_file(filepath):
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
