import logging
from extraction_engine.managers.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from database.database_setup import initial_setup as db_initial_setup
from extraction_engine.managers.exam_manager import ExamManager
from extraction_engine.managers.file_manager import FileManager
from utilities.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
def run_extraction(exam_format: str, question_pdf_path: str, answer_pdf_path: str):
    """Runs the exam extraction process."""
    logger.info("Starting exam extraction process")
    valid_formats = ConfigManager.get_all_exam_formats()
    if exam_format not in valid_formats:
        raise ValueError(f"Invalid exam_format: {exam_format}. Valid formats are: {valid_formats}")

    # Get the pdf paths using FileManager
    upload_path = FileManager.get_filepaths("uploads")
    question_pdf_path = upload_path.joinpath(question_pdf_path).as_posix()
    answer_pdf_path = upload_path.joinpath(answer_pdf_path).as_posix()

    # Fetch the db_path using FileManager
    db_path = FileManager.get_filepaths("database")
    db_manager = DatabaseManager(db_path)
    db_initial_setup(db_manager)
    logger.info(f"Using database: {db_path.as_posix()}")
    exam_manager = ExamManager(exam_format, question_pdf_path, answer_pdf_path, db_manager)
    status = exam_manager.process()
    return status