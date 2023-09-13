from PIL import Image
import re
import pytesseract

class OCRProcessor():
    
    @staticmethod
    def get_text_from_image(self, image: Image, psm_mode: int=3) -> str:
        """Extracts text from an image"""
        text = pytesseract.image_to_string(image, config=f'--psm {psm_mode}')
        return text.strip()

    @staticmethod
    def get_number_from_image(self, image: Image, psm_mode:int=7) -> int:
        """Extracts a number from image or else returns None"""
        text = self.get_text_from_image(image, psm_mode)
        if text.isdigit():
            return int(text)
        return None