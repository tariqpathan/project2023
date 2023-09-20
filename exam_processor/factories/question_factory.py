from PIL import Image
from database.models import Exam, Question
from typing import Optional
import os
from exam_processor.managers.file_manager import FileManager, ImageFileManager

class QuestionFactory:
    def __init__(self, db_session, exam: Exam):
        self.db_session = db_session
        self.exam = exam

    def create_question(self, image: Image.Image, qnum: Optional[int]) -> Question:
        """creates a question object using the Question model"""
        # Attempt to create a new question without saving the image
        question = Question(exam=self.exam, number=qnum)
        # Construct the relative path based on the question's ID or other criteria
        filename = "some_criterion"
        image_path = FileManager.construct_path(filename)
        
        try:
            question.image_path = image_path
            self.db_session.add(question)
            ImageFileManager.store_image(image, filename)
        
        except Exception as e:
            self.db_session.rollback()
            # Remove the saved image if there's a failure after image save
            if question.image_path:
                os.remove(question.image_path)
            raise Exception(f"Error creating Question: {qnum} for ExamID: {question.exam_id}. Error: {e}")
        return question
