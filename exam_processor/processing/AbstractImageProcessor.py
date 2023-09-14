from abc import ABC, abstractmethod
from PIL import Image

class AbstractImageProcessor(ABC):
    def __init__(self, config: dict):
        self._config = config
        self.validated = False

        for key in self.required_keys():
            setattr(self, f'_{key}', self._config[key])

    @classmethod
    @abstractmethod
    def required_keys(cls):
        pass

    @abstractmethod
    def process(self, image: Image.Image) -> Image.Image:
        """Converts an image of a page and returns a list of question-images"""
        pass

    @abstractmethod
    @staticmethod
    def validate_image_config(self, image: Image.Image):
        """Validate ImageProcessor-specific configuration"""
        pass

    @staticmethod
    def _convert_to_grayscale_image(image:Image.Image) -> Image.Image:
        """Converts image to grayscale"""
        return image.convert('L')

    @staticmethod
    def _convert_to_binary_image(image: Image.Image, threshold: int) -> Image.Image:
        """
        Converts a grayscale image to a binary, using threshold value
        1 represents a white pixel, 0 represents black
        """
        return image.point(lambda x: 0 if x < threshold else 255, "1")
