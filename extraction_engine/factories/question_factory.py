from PIL import Image
from database.models import Exam, Question
from typing import Optional
import uuid
from extraction_engine.managers.image_file_handler import ImageFileHandler
from extraction_engine.managers.file_manager import FileManager

import logging

logger = logging.getLogger(__name__)

class QuestionFactory:

    FOLDER_NAME = "images"

    def __init__(self, db_session, exam: Exam):
        self.db_session = db_session
        self.exam = exam
        self.image_folder = FileManager.get_filepaths(self.FOLDER_NAME)

    def create_question(self, image: Image.Image, qnum: Optional[int]) -> Question:
        """creates a question object using the Question model"""
        # Attempt to create a new question without saving the image
        question = Question(exam=self.exam, question_number=qnum)
        # Construct the relative path based on the question's ID or other criteria
        filename = self._generate_filename()
        question.image_filename = filename
        # logging.debug(f"Question image path: {question.image_filename}. qnum: {qnum}")
        try:
            self.db_session.add(question)
            ImageFileHandler.save_image(image, filename)
        
        except Exception as e:
            self.db_session.rollback()
            # Remove the saved image if there's a failure after image save
            ImageFileHandler.delete_image(filename)
            raise Exception(f"Error creating Question: {qnum} for ExamID: {question.exam_id}. Error: {e}")
        return question

    def _generate_filename(self, format: str="jpg") -> str:
        """Generates a filename for the image"""
        unique_id = uuid.uuid4()
        return f"{self.exam.year}-{self.exam.unit_code}{self.exam.component_code}-{unique_id}.{format}"
    