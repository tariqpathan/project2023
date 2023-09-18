from typing import Optional, Tuple
import PyPDF4
import re
import json
from exam_processor.managers.config_manager import ConfigManager
from exam_processor.pdf_processing.pdf_operations import PDFUtils
from exam_processor.processing.pdf_processor import first_page_text

class PDFManager:
    def __init__(self, exam_board: str, config_manager: ConfigManager):
        self.exam_board = exam_board
        self.settings = self._get_settings()
        self.config_manager = config_manager

    def _get_settings(self) -> dict:
        try:
            return self.config_manager.get_config("coverpage_settings", self.exam_board)
        except ValueError as e:
            raise e
        
    def load_pdfs(self, question_pdf_path: str, answer_pdf_path: str) -> Tuple[PyPDF4.PdfFileReader, PyPDF4.PdfFileReader]:
        """Loads the provided PDFs and returns them as PyPDF4 objects."""
        question_pdf = PDFUtils.load_pdf(question_pdf_path)
        answer_pdf = PDFUtils.load_pdf(answer_pdf_path)
        return question_pdf, answer_pdf

    def validate_pdfs(self, question_pdf: PyPDF4.PdfFileReader, answer_pdf: PyPDF4.PdfFileReader) -> bool:
        """Extracts the cover pages from the provided PDFs and checks whether they match."""
        question_text, answer_text = self._parse_cover_page(question_pdf, answer_pdf)
        question_data = self._extract(question_text, "question")
        answer_date = self._extract(answer_text, "answer")
        return question_data["exam_series"] == answer_date["exam_series"]

    def _parse_cover_page(self, question_pdf, answer_pdf):
        """Extracts the cover pages from the provided PDFs and returns their text."""
        question_cover_text = first_page_text(question_pdf)
        answer_cover_text = first_page_text(answer_pdf)
        return question_cover_text, answer_cover_text
    
    def _extract(self, text: str, paper: str) -> dict:
        """Extracts the exam series from the cover page text."""
        extraction_config = self.settings['regex'][paper]
        capture_groups = extraction_config['capture_groups']
        regex = extraction_config['regex']

        match = re.search(regex, text)
        if not match:
            raise ValueError(f"No match found for the given regex of {self.exam_board}.")

        extracted_data = {}
        for group_name in capture_groups:
            extracted_data[group_name] = match.group(group_name)

        return extracted_data
    
    def _return_pdf_images(self, pdf_path: str) -> list:
        """Returns a list of images from a PDF file."""
        return PDFUtils.convert_to_images(pdf_path)
    
    def _return_pdf_text(self, pdf_path: str) -> str:
        """Returns the text from a PDF file."""
        return PDFUtils.extract_text_except_first_page(pdf_path)

    def main(self, question_pdf_path: str, answer_pdf_path: str):
        """Returns a list of questions and answers from the provided PDFs."""
        question_pdf, answer_pdf = self.load_pdfs(question_pdf_path, answer_pdf_path)
        valid = self.validate_pdfs(question_pdf, answer_pdf)
        if valid:
            questions = self._return_pdf_images(question_pdf_path)[1:]
            answers = self._return_pdf_text(answer_pdf_path)
            return questions, answers
        else:
            raise ValueError(f"Question paper {question_pdf_path} does not match" \
                             f"answer paper {answer_pdf_path}.")

