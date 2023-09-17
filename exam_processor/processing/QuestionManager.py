from PIL import Image
from typing import Dict, List, Tuple, Optional
from database.models import Exam
from exam_processor.QuestionFactory import QuestionFactory

from exam_processor.processing.AbstractImageProcessor import AbstractImageProcessor
from exam_processor.processing.CambridgeScienceImageProcessor import CambridgeScienceImageProcessor
from exam_processor.processing.TextProcessor import TextProcessor

class QuestionManager:
    def __init__(self, exam_board, config) -> None:
        self.config = config
        self.exam_board = exam_board
        self.image_processor = self._get_image_processor(exam_board)
        self.text_processor = self._get_text_processor(exam_board)
        self.question_factory = None

    def _get_image_processor(self, exam_board: str) -> AbstractImageProcessor:
        """
        Returns an instance of the required image processor based on the document type.
        """
        # TODO: change this to a factory
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
        return self.image_processor.extract(image)

    def _get_question_number(self, image: Image.Image) -> Optional[int]:
        """Extracts question number from a question image."""
        number = self.text_processor.get_question_number(image)
        return number

    def _post_process(self, image: Image.Image):
        """Modifies image after extracting data"""
        coords = self.config[self.exam_board]["textProcessor"]
        return self.image_processor.post_process(image, coords)

    def set_question_factory(self, db_session, exam: Exam) -> QuestionFactory:
        """Returns a QuestionFactory object"""
        return QuestionFactory(db_session, exam)

    def _create_question(self, image: Image.Image, qnum: Optional[int]):
        """Creates a Question object using the Question model"""
        if self.question_factory:
            self.question_factory.create_question(image, qnum)
        else:
            raise Exception("QuestionFactory not set")
    
    def _process_images(self, images: List[Image.Image]):
        """Processes a list of images and returns a list of questions"""
        questions = []
        for image in images:
            questions.extend(self._extract_questions(image))

        question_nums = []
        post_processed_images = []
        for image in questions:
            question_nums.append(self._get_question_number(image))
            post_processed_images.append(self._post_process(image))

        return zip(question_nums, post_processed_images)

    def execute(self, db_session, exam: Exam, images: List[Image.Image]):
        """Executes the question processing pipeline"""
        self.set_question_factory(db_session, exam)
        question_nums, processed_images = self._process_images(images)
        for qnum, image in zip(question_nums, processed_images):
            self._create_question(image, qnum)
