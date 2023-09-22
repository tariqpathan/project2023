from pathlib import Path
from file_manager import FileManager


class ImageFileManager:

    @staticmethod
    def get_image_save_path(filename: str) -> Path:
        """Returns the path where the image should be saved."""
        #TODO: avoid hardcoding the path
        base_path = FileManager.construct_path("static/question_images")
        return FileManager.construct_path(filename)

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