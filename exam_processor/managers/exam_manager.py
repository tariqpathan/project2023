from exam_processor import ConfigManager
from exam_processor import PDFManager
from exam_processor import close_pdf


class ExamManager:
    def __init__(self, config_path: str, db_path: str):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.get_config()
        self.config_manager.validate()

        self.pdf_manager = PDFManager()
        
        self.db_manager = DatabaseManager(db_path)
        self.db_session = self.db_manager.get_session()
        
        self.question_manager = QuestionManager(self.config["exam_board"], self.config)
        self.answer_manager = AnswerManager(self.config)

    def process_exam(self, question_file_path: str, answer_file_path: str):
        question_pdf = self.pdf_manager.load_pdf(question_file_path)
        answer_pdf = self.pdf_manager.load_pdf(answer_file_path)

        if not self.pdf_manager.validate_pdfs(question_pdf, answer_pdf):
            raise ValueError("Mismatch between question and answer files or invalid file format.")

        question_cover, answer_cover = self.pdf_manager.parse_cover_pages(question_pdf, answer_pdf)

        if not self.pdf_manager.match_cover_pages(question_cover, answer_cover):
            raise ValueError("Mismatched exam series in question and answer files.")

        # Rest of the processing logic
        # ...

        # Don't forget to close the PDFs
        close_pdf(question_pdf)
        close_pdf(answer_pdf)
        
        # Commit to the database.
        self.db_session.commit()
