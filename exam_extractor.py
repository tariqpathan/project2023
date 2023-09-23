# exam_extraction.py

from extraction_engine.managers.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from extraction_engine.managers.exam_manager import ExamManager
from extraction_engine.managers.file_manager import FileManager
import logging

logger = logging.getLogger(__name__)

def run_exam_extraction(exam_format: str, question_pdf_path: str, answer_pdf_path: str):
    """Runs the exam extraction process."""
    ConfigManager()
    valid_formats = ConfigManager.get_all_exam_formats()
    logger.debug(f"Valid formats: {valid_formats}")
    if exam_format not in valid_formats:
        raise ValueError(f"Invalid exam_format: {exam_format}. Valid formats are: {valid_formats}")

    # Get the pdf paths using FileManager
    upload_path = FileManager.get_filepaths("uploads")
    question_pdf_path = upload_path.joinpath(question_pdf_path).as_posix()
    answer_pdf_path = upload_path.joinpath(answer_pdf_path).as_posix()

    # Fetch the db_path using FileManager
    db_path = FileManager.get_filepaths("db_path")
    db_path_str = db_path.as_posix()
    db_manager = DatabaseManager(db_path_str)
    logger.info(f"Using database: {db_path_str}")
    exam_manager = ExamManager(exam_format, question_pdf_path, answer_pdf_path, db_manager)
    exam_manager.process()

if __name__ == "__main__":
    exam_format = "cambridge_science"
    run_exam_extraction(exam_format, 'phys-062511-may2016.pdf', 'phys-062511-may2016-ms.pdf')