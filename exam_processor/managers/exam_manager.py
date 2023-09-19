from database.database_manager import DatabaseManager
from exam_processor import ConfigManager
from exam_processor import PDFManager
from exam_processor.exam_factory import ExamFactory
from exam_processor.managers.answer_manager import AnswerManager
from exam_processor.managers.file_manager import FileHandler, ImageFileManager
from exam_processor.managers.question_manager import QuestionManager


class ExamManager:
    def __init__(self, exam_board: str, question_pdf_path: str, answer_pdf_path: str, 
                 db_path: str):
        self.exam_board = exam_board
        self.question_pdf_path = question_pdf_path
        self.answer_pdf_path = answer_pdf_path
        self.file_handler = FileHandler()
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager(db_path)
        # self.db_functions = Databas(db_path)
        self.pdf_manager = PDFManager(exam_board, self.config_manager)
        self.question_manager = QuestionManager(exam_board, self.config_manager.get_config("question_manager", exam_board))
        self.answer_manager = AnswerManager(exam_board)

    # TODO: use file_handler to construct the paths

    def validate_exam_board(self):
        """Validates the exam board."""
        if self.exam_board not in self.db_functions.get_exam_boards():
            raise ValueError(f"Unsupported exam board: {self.exam_board}")
    
    def _validate_exam_details(self, data: dict):
        """Validates the exam details."""
        pass

    def process(self, exam_data: dict):
        try:
            with self.db_manager as db_session:
                self.validate_exam_board()
                #TODO: validate exam details
                #TODO: load and validate file paths
                #TODO: extract exam details from pdfs
                #TODO: retirieve subject id
                #TODO: validate exam details
                #TODO: create exam
                #TODO: run question manager
                #TODO: run answer manager
                #TODO: commit session
                exam_factory = ExamFactory(db_session)
                exam = exam_factory.create_exam(exam_data)

                data = self.pdf_manager.extract_pdf_data(self.question_pdf_path, self.answer_pdf_path)

                question_manager_config = self.config_manager.get_config("question_manager", self.exam_board)
                question_manager = QuestionManager(self.exam_board, question_manager_config)
                question_manager.execute(db_session, exam, questions_images) 

                # Similar logic for answers (using a hypothetical AnswerManager)

                # After everything is done, commit the session.
                self.db_manager.commit()

        except Exception as e:
            # If any error occurs, rollback the session.
            self.db_manager.rollback()
            # Handle or re-raise the exception as needed.
            raise e
