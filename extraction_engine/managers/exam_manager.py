from database.database_manager import DatabaseManager
from database.models import Exam, Question, Subject
from database.database_utils import get_exam
from extraction_engine.managers.config_manager import ConfigManager
from extraction_engine.pdf_processing.pdf_manager import PDFManager
from extraction_engine.factories.exam_factory import ExamFactory
from extraction_engine.managers.answer_manager import AnswerManager
from extraction_engine.managers.question_manager import QuestionManager
import logging
from typing import List

logger = logging.getLogger(__name__)

class ExamManager:
    def __init__(self, exam_format: str, question_pdf_path: str, answer_pdf_path: str, 
                 db_manager: DatabaseManager):
        self.exam_format = exam_format
        self.question_pdf_path = question_pdf_path
        self.answer_pdf_path = answer_pdf_path

        # self.config_manager = ConfigManager()
        self.db_manager = db_manager
        logger.debug("Setting PDFManager")
        self.pdf_manager = PDFManager(exam_format)
        logger.debug("Setting QuestionManager")
        self.question_manager = QuestionManager(exam_format)
        logger.debug("Setting AnswerManager")
        self.answer_manager = AnswerManager(exam_format)

    def _get_or_create_exam(self, db_session, exam_data: dict) -> Exam:
        # Try to fetch an existing exam based on the unique constraint
        exam = get_exam(db_session, exam_data)

        if exam is None:
            exam_factory = ExamFactory()
            exam = exam_factory.get_or_create_exam(session=db_session, exam_data=exam_data)
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
        logger.info(f"Processing exam: {self.exam_format}")
        try:
            logger.info("Extracting data from PDFs...")
            data = self._extract_data_from_pdfs()
            exam_data = data["cover_details"]
            raw_questions = data["questions"]
            raw_answers = data["answers"]
            logger.info(f'Exam data: {exam_data}')
            
            with self.db_manager.get_session() as db_session:
                exam = self._get_or_create_exam(db_session, exam_data)
                logging.debug(f"Exam: {exam}")
                questions = self._process_questions(db_session, exam, raw_questions)
                self._process_answers(db_session, raw_answers, questions)
                db_session.commit()

        except Exception as e:
            # If any error occurs, rollback the session.
            if self.db_manager.session:
                self.db_manager.session.rollback()
            raise e
