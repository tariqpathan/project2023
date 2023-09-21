from PIL import Image
from typing import Dict, List, Tuple, Optional
from database.models import Exam, Question
from exam_processor.managers.config_manager import ConfigManager
from exam_processor.question_factory import QuestionFactory

from exam_processor.processing.AbstractImageProcessor import AbstractImageProcessor
from exam_processor.processing.CambridgeScienceImageProcessor import CambridgeScienceImageProcessor
from exam_processor.processing.ImageTextProcessor import ImageTextProcessor

class QuestionManager:
    def __init__(self, exam_format) -> None:
        self.exam_format = exam_format
        self.image_processor = self._get_image_processor(exam_format)
        self.text_processor = self._get_text_processor(exam_format)
        self.question_factory = None
        self.config = ConfigManager().get_config("question_manager", exam_format)

    def _get_image_processor(self, exam_format: str) -> AbstractImageProcessor:
        """
        Returns an instance of the required image processor based on the document type.
        """
        # TODO: change this to a factory
        if exam_format == "cambridge_science":
            return CambridgeScienceImageProcessor(self.config[exam_format]["imageProcessor"])
        else:
            raise ValueError(f"Unsupported exam board: {exam_format}")

    def _get_text_processor(self, exam_format: str) -> ImageTextProcessor:
        """
        Returns an instance of the required OCR processor based on the ocr type.
        """
        if not exam_format: return ImageTextProcessor(self.config[exam_format]["textProcessor"])
        else:
            raise ValueError(f"Unsupported OCR type: {exam_format}")

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
        coords = self.config[self.exam_format]["textProcessor"]
        return self.image_processor.post_process(image, coords)

    def set_question_factory(self, db_session, exam: Exam) -> QuestionFactory:
        """Returns a QuestionFactory object"""
        return QuestionFactory(db_session, exam)

    def _create_question(self, image: Image.Image, qnum: Optional[int]) -> Question:
        """Creates a Question object using the Question model"""
        if self.question_factory:
            return self.question_factory.create_question(image, qnum)
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

    def execute(self, db_session, exam: Exam, images: List[Image.Image]) -> List[Question]:
        """Executes the question processing pipeline"""
        self.set_question_factory(db_session, exam)
        question_nums, processed_images = self._process_images(images)
        # for qnum, image in zip(question_nums, processed_images):
        #     self._create_question(image, qnum)
        return [self._create_question(i, q) for i, q in zip(processed_images, question_nums)]