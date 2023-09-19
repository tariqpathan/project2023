from typing import Dict, Optional, Tuple
import PyPDF4
import re
from exam_processor.managers.config_manager import ConfigManager
from exam_processor.pdf_processing.pdf_utils import PDFUtils

class PDFManager:
    def __init__(self, exam_board: str, config_manager: ConfigManager):
        self.exam_board = exam_board
        self.settings = self._get_settings()
        self.config_manager = config_manager

    def _get_settings(self) -> dict:
        try: #TODO: remove this try-except block
            return self.config_manager.get_config("coverpage_settings", self.exam_board)
        except ValueError as e:
            raise e
        
    def _validate_pdfs(self, question_pdf: PyPDF4.PdfFileReader, answer_pdf: PyPDF4.PdfFileReader) -> bool:
        """Extracts the cover pages from the provided PDFs and checks whether they match."""
        question_text = PDFUtils.first_page_text(question_pdf)
        answer_text = PDFUtils.first_page_text(answer_pdf)
        question_data = self._extract(question_text, "question")
        answer_data = self._extract(answer_text, "answer")
        return question_data["exam_series"] == answer_data["exam_series"]

    def _extract(self, text: str, paper: str) -> dict:
        """Extracts the exam series from the cover page text."""
        extraction_config = self.settings['regex'][paper]
        capture_groups = extraction_config['capture_groups']
        regex = extraction_config['regex']

        match = re.search(regex, text)
        if not match:
            raise ValueError(f"No match found for the given regex of {self.exam_board}.")

        extracted_data = {}
        for group_name in capture_groups: #TODO: what happens if capture_groups are empty?
            extracted_data[group_name] = match.group(group_name)
        return extracted_data
    
    def _return_pdf_images(self, pdf_path: str) -> list:
        """Returns a list of images from a PDF file, excluding the cover page."""
        return PDFUtils.convert_to_images(pdf_path)
    
    def _return_pdf_text(self, pdf_path: str) -> str:
        """Returns all the text from a PDF file, excluding the cover page."""
        return PDFUtils.extract_text_except_first_page(pdf_path)

    def _get_exam_cover_details(self, pdf: PyPDF4.PdfFileReader) -> Dict[str, str|int]:
        text = PDFUtils.first_page_text(pdf)
        return self._extract(text, "question")

    def extract_pdf_data(self, question_pdf_path: str, answer_pdf_path: str) -> Tuple[Dict[str, str|int], list, str]:
        """
        Extracts cover details as a dict, images of the question paper as a list, 
        and the answer text as a string. Returns as a tuple of three elements.
        """
        question_pdf = PDFUtils.load_pdf(question_pdf_path)
        answer_pdf = PDFUtils.load_pdf(answer_pdf_path)
        try:
            valid = self._validate_pdfs(question_pdf, answer_pdf)
            if valid:
                cover_details = self._get_exam_cover_details(question_pdf)
                questions = self._return_pdf_images(question_pdf_path)[1:]
                answers = self._return_pdf_text(answer_pdf_path)
                return cover_details, questions, answers
            else:
                raise ValueError("The PDFs do not match.")
        except Exception as e:
            raise e
        finally:
            PDFUtils.close_pdf(question_pdf)
            PDFUtils.close_pdf(answer_pdf)
    