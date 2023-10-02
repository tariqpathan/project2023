from PIL import Image
from typing import List, Optional
from database.models import Exam, Question
from extraction_engine.managers.config_manager import ConfigManager
from extraction_engine.factories.image_processor_factory import ImageProcessorFactory
from extraction_engine.factories.question_factory import QuestionFactory
from extraction_engine.processing.abstract_image_processor import AbstractImageProcessor
from extraction_engine.processing.image_text_processor import ImageTextProcessor

import logging

logger = logging.getLogger(__name__)

class QuestionManager:
    def __init__(self, exam_format) -> None:
        self.exam_format = exam_format
        cm = ConfigManager()
        self.config = cm.get_config(exam_format=exam_format, config_type="exam_formats")
        # logging.debug(f"self.config in QuestionManager: {self.config}")
        self.image_processor = self._get_image_processor()
        self.text_processor = self._get_text_processor()
        self.question_factory = None

    def _get_image_processor(self) -> AbstractImageProcessor:
        """
        Returns an instance of the required image processor based on the document type.
        """
        return ImageProcessorFactory.create_processor(self.exam_format, self.config["imageProcessor"])

    def _get_text_processor(self) -> ImageTextProcessor:
        """
        Returns an instance of the required OCR processor based on the ocr type.
        """
        return ImageTextProcessor(self.config["textProcessor"])
    
    def validate_processor(self, image: Image.Image) -> None:
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
        coords = self.config["textProcessor"]
        return self.image_processor.post_process(image, coords)

    def _set_question_factory(self, db_session, exam: Exam) -> None:
        """Returns a QuestionFactory object"""
        self.question_factory = QuestionFactory(db_session, exam)

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

        return (question_nums, post_processed_images)

    def execute(self, db_session, exam: Exam, images: List[Image.Image]) -> List[Question]:
        """Executes the question processing pipeline"""
        logging.debug("Executing question processing pipeline")
        self._set_question_factory(db_session, exam)
        self.validate_processor(images[0])
        question_nums, processed_images = self._process_images(images)
        logging.info(f"Number of questions: {len(question_nums)}, number of images: {len(processed_images)}")
        return [self._create_question(i, q) for i, q in zip(processed_images, question_nums)]