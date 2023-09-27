from pathlib import Path

from PIL import Image

from extraction_engine.managers.file_manager import FileManager


class ImageFileHandler:
    IMAGE_FORMAT = "jpg"

    @staticmethod
    def get_image_path(filepath: str) -> Path:
        """Returns the path where the image should be saved."""
        base_path = FileManager.get_filepaths("images")  # get the base path for images from FileManager
        return FileManager.construct_path(filepath, str(base_path))  # construct the full path using FileManager

    @classmethod
    def save_image(cls, image: Image.Image, filename: str) -> Path:
        """Saves the given image data to the specified filename in the image directory."""
        image_save_path = ImageFileHandler.get_image_path(filename)
        try:
            image.save(image_save_path)
            return image_save_path
        except Exception as e:
            raise IOError(f"Unable to save image: {e}")

    @staticmethod
    def get_image(filename: str) -> bytes:
        """Returns the image data for the specified filename."""
        image_path = ImageFileHandler.get_image_path(filename)
        try:
            with open(image_path, 'rb') as image_file:
                return image_file.read()
        except FileNotFoundError:
            raise ValueError(f"Image file {image_path} not found.")
        except Exception as e:
            raise IOError(f"Unable to read image: {e}")

    @staticmethod
    def delete_image(filename: str) -> None:
        """Deletes the image with the specified filename."""
        image_path = ImageFileHandler.get_image_path(filename)
        if not image_path.exists(): return
        try:
            image_path.unlink()
        except FileNotFoundError:
            raise ValueError(f"Image file {image_path} not found.")
        except Exception as e:
            raise IOError(f"Unable to delete image: {e}")
