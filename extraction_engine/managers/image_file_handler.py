from pathlib import Path
from file_manager import FileManager

class ImageFileManager:

    @staticmethod
    def get_image_save_path(filepath: str) -> Path:
        """Returns the path where the image should be saved."""
        base_path = FileManager.get_filepaths("images")  # get the base path for images from FileManager
        return FileManager.construct_path(filepath, str(base_path))  # construct the full path using FileManager

    @staticmethod
    def save_image(image_data, filename: str):
        """Saves the given image data to the specified filename in the image directory."""
        save_path = ImageFileManager.get_image_save_path(filename)
        
        try:
            with open(save_path, 'wb') as image_file:
                image_file.write(image_data)
        except Exception as e:
            raise IOError(f"Unable to save image: {e}")
    
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