from PIL import Image
from database.models import Exam, Question
from typing import Optional
import os
import time
from extraction_engine.managers.image_file_handler import ImageFileManager
from extraction_engine.managers.file_manager import FileManager

class QuestionFactory:
    def __init__(self, db_session, exam: Exam):
        self.db_session = db_session
        self.exam = exam

    def create_question(self, image: Image.Image, qnum: Optional[int]) -> Question:
        """creates a question object using the Question model"""
        # Attempt to create a new question without saving the image
        question = Question(exam=self.exam, number=qnum)
        # Construct the relative path based on the question's ID or other criteria
        filename = self._generate_filename()
        image_path = FileManager.construct_path(filename)
        question.image_path = image_path
        
        try:
            self.db_session.add(question)
            ImageFileManager.save_image(image, filename)
        
        except Exception as e:
            self.db_session.rollback()
            # Remove the saved image if there's a failure after image save
            if question.image_path:
                os.remove(question.image_path)
            raise Exception(f"Error creating Question: {qnum} for ExamID: {question.exam_id}. Error: {e}")
        return question

    def _generate_filename(self) -> str:
        """Generates a filename for the image"""
        timestamp = int(time.time() * 1000)
        return f"{self.exam.id}-{self.exam.unit_code, self.exam.unit_code}-{timestamp}"