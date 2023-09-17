from abc import ABC, abstractmethod
from PIL import Image
from typing import Dict, List

class AbstractImageProcessor(ABC):
    EXAM_BOARD = ""
    REQUIRED_PARAMS: List[str] = []

    def __init__(self, config: Dict):
        self._config = config

    @abstractmethod
    def _derive_attributes(self):
        """Derive and set specific attributes from the configuration parameters."""
        pass

    @abstractmethod
    def extract(self, image: Image.Image) -> List[Image.Image]:
        """Converts an image of a page and returns a list of question-images"""
        pass

    @abstractmethod
    def post_process(self, image: Image.Image, *args) -> Image.Image:
        """Modifies images after data has been extracted"""
        pass
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "EXAM_BOARD"):
            raise TypeError(f"Subclasses of AbstractImageProcessor must have an "\
                "'EXAM_BOARD' attribute. {cls.__name__} doesn't.")

    @abstractmethod
    def validate(self, image:Image.Image):
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
    