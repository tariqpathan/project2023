from typing import List, Dict, Tuple
from PIL import Image
import numpy as np
from abc import ABC, abstractmethod

class QuestionProcessor:
    image_processors = {
        "cambridge_science": CambridgeScienceImageProcessor,
        "aqa_maths": AqaMathsImageProcessor,
    }

    def _initialize_image_processor(self, board_name: str):
        if board_name not in self.image_processors:
            raise ValueError(f"Unsupported board: {board_name}")
        return self.image_processors[board_name]()


    def __init__(self, image_width: int, image_height: int, margin: Tuple[int, int]):
        self.image_width = image_width
        self.image_height = image_height
        self.margin = margin

    @abstractmethod
    def create_image_arrays(self, binary_image: Image.Image) -> Dict[str, np.ndarray]:
        pass

    @abstractmethod
    def detect_question_start(self, binary_array, cropped_array, question_spacing=25) -> np.ndarray:
        pass

    @abstractmethod
    def get_question_coordinates(self, ques_start_rows: np.ndarray) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def create_question(self, ):
        pass

    @staticmethod
    def crop_image(self, image: Image.Image, width: Tuple[int, int], coords: List[Tuple[int, int]]) -> List[Image.Image]:
        (xstart, xend) = width
        return [image.crop((xstart, ystart, xend, yend)) for (ystart, yend) in coords]

    @staticmethod
    def remove_vertical_whitespace(image: Image.Image, padding:int, threshold: int) -> Image.Image:
        """Removes vertical whitespace from an image up to a padded amount"""
        data = np.array(image)
        min_values = data.min(axis=1)
        non_white_rows = np.where(min_values < threshold)[0]
        top = max(non_white_rows[0] - padding, 0)
        bottom = min(non_white_rows[-1] + padding, image.height)
        return image.crop((0, top, image.width, bottom))
