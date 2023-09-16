from PIL import Image
from typing import Dict, List, Tuple, Optional
import pytesseract

from exam_processor.processing.AbstractImageProcessor import AbstractImageProcessor
from exam_processor.processing.CambridgeScienceImageProcessor import CambridgeScienceImageProcessor
from exam_processor.processing.OCRProcessor import OCRProcessor

class QuestionProcessor:
    def __init__(self, name, config) -> None:
        self.config = config
        self.image_processor = self._get_image_processor(name)
        self.ocr_processor = self._get_ocr_processor(name)

    def _get_image_processor(self, exam_board: str) -> Optional[AbstractImageProcessor]:
        """
        Returns an instance of the required image processor based on the document type.
        """
        if exam_board == "cambridge_science":
            return CambridgeScienceImageProcessor(self.config["cambridge_science"]["imageProcessor"])
        else:
            raise ValueError(f"Unsupported exam board: {exam_board}")

    def _get_ocr_processor(self, ocr_type: str) -> Optional[OCRProcessor]:
        """
        Returns an instance of the required OCR processor based on the ocr type.
        """
        if not ocr_type: return OCRProcessor()
        else:
            raise ValueError(f"Unsupported OCR type: {ocr_type}")

    def extract_questions(self, page_image: List[Image.Image]) -> List[Image.Image]:
        """
        Extracts individual question images from a page along with their respective question numbers.
        Returns a list of images corresponding to a single question.
        """
        pass

        # pass a single image to the image_processor

        self.image_processor.validate() # pass in image processor configurations        
        # only call the process and post-process methods


        # Extracting question numbers

        # return list(zip(question_numbers, question_images))

    def get_text_from_question(self, question_image: Image.Image) -> str:

        """
        Extracts text from a question image.
        """
        pass


    @staticmethod
    def load_configs(self, config):
        self.config = config