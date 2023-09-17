from PIL import Image
from exam_processor.models import Question
import os

from file_handler import save_image

class QuestionFactory:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_question(self, image: Image.Image, exam_id: int) -> Question:
        """creates a question object using the Question model"""
        # Attempt to create a new question without saving the image
        question = Question(exam_id=exam_id)
        self.db_session.add(question)
        
        # Save the changes to the database (this might raise an exception)
        try:
            self.db_session.commit()
            
            # Construct the relative path based on the question's ID or other criteria
            relative_path = "some_criterion"
            
            # Save the image and update the image_path
            image_path = save_image(image, relative_path)
            question.image_path = image_path
            
            # Save the changes again
            self.db_session.commit()
        except Exception as e:
            # Rollback any changes in the event of an error
            self.db_session.rollback()
            
            # Remove the saved image if there's a failure after image save
            if question.image_path:
                os.remove(question.image_path)
            
            # Raise the original exception to notify callers
            raise e
        
        return question
