from database.database_manager import DatabaseManager
from database.models import Answer, Exam, Question, Subject
from exam_processor import ConfigManager
from exam_processor import PDFManager
from exam_processor.exam_factory import ExamFactory
from exam_processor.managers.answer_manager import AnswerManager
from exam_processor.managers.file_manager import FileHandler, ImageFileManager
from exam_processor.managers.question_manager import QuestionManager
from typing import List

class ExamManager:
    def __init__(self, exam_board: str, question_pdf_path: str, answer_pdf_path: str, 
                 db_path: str):
        self.exam_board = exam_board
        self.question_pdf_path = question_pdf_path
        self.answer_pdf_path = answer_pdf_path

        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager(db_path)
        
        self.pdf_manager = PDFManager(exam_board, self.config_manager)
        self.question_manager_config = self.config_manager.get_config("question_manager", exam_board)
        self.question_manager = QuestionManager(exam_board, self.question_manager_config)
        self.answer_manager = AnswerManager(exam_board)

    def validate_exam_board(self):
        """Validates the exam board."""
        # TODO: Implement this method
        pass

    def validate_exam_details(self, exam_data: dict):
        """Validates the exam details."""
        # TODO: Implement this method
        pass

    def get_or_create_exam(self, exam_data: dict) -> Exam:
        # Try to fetch an existing exam based on the unique constraint
        exam = self.db_session.query(Exam).filter_by(**exam_data).first()

        if exam is None:
            exam_factory = ExamFactory()
            exam = exam_factory.create_exam(exam_data)
            self.db_session.add(exam)
        return exam


    def extract_data_from_pdfs(self):
        """Extracts data from PDFs."""
        return self.pdf_manager.extract_pdf_data(self.question_pdf_path, self.answer_pdf_path)

    def process_questions(self, db_session, exam, questions_images):
        """Process questions."""
        self.question_manager.execute(db_session, exam, questions_images)

    def process_answers(self, db_session, text: str, questions: List[Question]):
        """Process answers."""
        self.answer_manager.execute(db_session, text, questions)

    def process(self, exam_data: dict):
        try:
            with self.db_manager.get_session() as db_session:
                self.validate_exam_board()
                self.validate_exam_details(exam_data)

                exam_factory = ExamFactory()
                exam = exam_factory.create_exam(exam_data)

                data = self.extract_data_from_pdfs()

                # Assuming questions_images is part of the data, or replace it accordingly.
                questions_images = data.get('questions_images', [])

                self.process_questions(db_session, exam, questions_images)
                self.process_answers()

                db_session.commit()

        except Exception as e:
            # If any error occurs, rollback the session.
            if self.db_manager.session:
                self.db_manager.session.rollback()
            raise e
