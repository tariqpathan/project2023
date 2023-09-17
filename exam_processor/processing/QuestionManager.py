from PIL import Image
from typing import Dict, List, Tuple, Optional
import pytesseract

from exam_processor.processing.AbstractImageProcessor import AbstractImageProcessor
from exam_processor.processing.CambridgeScienceImageProcessor import CambridgeScienceImageProcessor
from exam_processor.processing.TextProcessor import TextProcessor

class QuestionProcessor:
    def __init__(self, exam_board, config) -> None:
        self.config = config
        self.exam_board = exam_board
        self.image_processor = self._get_image_processor(exam_board)
        self.text_processor = self._get_text_processor(exam_board)

    def _get_image_processor(self, exam_board: str) -> AbstractImageProcessor:
        """
        Returns an instance of the required image processor based on the document type.
        """
        if exam_board == "cambridge_science":
            return CambridgeScienceImageProcessor(self.config[exam_board]["imageProcessor"])
        else:
            raise ValueError(f"Unsupported exam board: {exam_board}")

    def _get_text_processor(self, exam_board: str) -> TextProcessor:
        """
        Returns an instance of the required OCR processor based on the ocr type.
        """
        if not exam_board: return TextProcessor(self.config[exam_board]["textProcessor"])
        else:
            raise ValueError(f"Unsupported OCR type: {exam_board}")

    def validate_processor(self, image: Image.Image):
        self.image_processor.validate(image)

    def _extract_questions(self, image: Image.Image) -> List[Image.Image]:
        """Extracts individual question images from an image of questions """
        return self.image_processor.process(image)

    def _get_question_number(self, image: Image.Image) -> Optional[int]:
        """Extracts question number from a question image."""
        number = self.text_processor.get_question_number(image)
        return number

    def _post_process(self, image: Image.Image):
        """Modifies image after extracting data"""
        coords = self.config[self.exam_board]["textProcessor"]
        return self.image_processor.post_process(image, coords)

    def _create_question(self, number: Optional[int], image: Image.Image):
        """Creates a Question object using the Question model"""

    def _save_image(self, image: Image.Image) -> str:
        """Saves the question image to a predetermined location and returns filepath"""
        return ""

    
