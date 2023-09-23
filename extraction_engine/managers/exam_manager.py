from database.database_manager import DatabaseManager
from database.models import Exam, Question, Subject
from exam_processor.managers.config_manager import ConfigManager
from exam_processor.pdf_processing.pdf_manager import PDFManager
from exam_processor.factories.exam_factory import ExamFactory
from exam_processor.managers.answer_manager import AnswerManager
from exam_processor.managers.question_manager import QuestionManager
from typing import List

class ExamManager:
    def __init__(self, exam_format: str, question_pdf_path: str, answer_pdf_path: str, 
                 db_path: str):
        self.exam_format = exam_format
        self.question_pdf_path = question_pdf_path
        self.answer_pdf_path = answer_pdf_path

        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager(db_path)
        
        self.pdf_manager = PDFManager(exam_format)
        self.question_manager = QuestionManager(exam_format)
        self.answer_manager = AnswerManager(exam_format)

    def _get_or_create_exam(self, db_session, exam_data: dict) -> Exam:
        # Try to fetch an existing exam based on the unique constraint
        exam = db_session.query(Exam).filter_by(**exam_data).first()
        if exam is None:
            exam_factory = ExamFactory()
            exam = exam_factory.create_exam(exam_data)
            db_session.add(exam)
        return exam

    def _extract_data_from_pdfs(self):
        """Extracts data from PDFs."""
        return self.pdf_manager.extract_pdf_data(self.question_pdf_path, self.answer_pdf_path)

    def _process_questions(self, db_session, exam, questions_images) -> List[Question]:
        """Process questions."""
        return self.question_manager.execute(db_session, exam, questions_images)

    def _process_answers(self, db_session, text: str, questions: List[Question]):
        """Process answers."""
        self.answer_manager.execute(db_session, text, questions)

    def process(self):
        try:
            with self.db_manager.get_session() as db_session:

                data = self._extract_data_from_pdfs()
                exam_data = data["cover_details"]
                raw_questions = data["questions"]
                raw_answers = data["answers"]

                exam = self._get_or_create_exam(db_session, exam_data)

                questions = self._process_questions(db_session, exam, raw_questions)
                self._process_answers(db_session, raw_answers, questions)

                db_session.commit()

        except Exception as e:
            # If any error occurs, rollback the session.
            if self.db_manager.session:
                self.db_manager.session.rollback()
            raise e