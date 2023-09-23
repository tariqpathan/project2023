from PIL import Image
import pytesseract
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ImageTextProcessor():
    def __init__(self, config: Dict):
        self._config = config
        self._xstart = config["question_x_start"]
        self._ystart = config["question_y_start"]
        self._xend = config["question_x_end"]
        self._yend = config["question_y_end"]
    
    def _question_crop(self, image: Image.Image):
        coords = (self._xstart, self._ystart, self._xend, self._yend)
        return image.crop(coords)

    @staticmethod
    def get_text_from_image(image: Image.Image, psm_mode: int=3) -> str:
        """Extracts text from an image"""
        text = pytesseract.image_to_string(image, config=f'--psm {psm_mode}')
        return text.strip()

    def get_question_number(self, image: Image.Image, psm_mode:int=7) -> Optional[int]:
        """Extracts a number from image or else returns None"""
        cropped = self._question_crop(image)
        text = ImageTextProcessor.get_text_from_image(cropped, psm_mode)
        if text.isdigit():
            return int(text)
        return None