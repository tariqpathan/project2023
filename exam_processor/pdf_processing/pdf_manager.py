from typing import Tuple
import PyPDF4
import re
import json
from exam_processor.pdf_processing.pdf_operations import PDFUtils
from exam_processor.processing.pdf_processor import first_page_text

class PDFManager:
    def __init__(self, exam_board: str):
        self.exam_board = exam_board
        self.settings = self._get_settings()

    def _get_settings(self) -> dict:
        #TODO: add in correct file location
        with open("config/coverpage_settings.json", "r") as file:
            all_settings = json.load(file)
            if all_settings[self.exam_board] is None:
                raise ValueError(f"No settings found for exam board: {self.exam_board}")
            return all_settings[self.exam_board]
        
    def load_pdfs(self, question_pdf_path: str, answer_pdf_path: str) -> Tuple[PyPDF4.PdfFileReader, PyPDF4.PdfFileReader]:
        question_pdf = PDFUtils.load_pdf(question_pdf_path)
        answer_pdf = PDFUtils.load_pdf(answer_pdf_path)
        return question_pdf, answer_pdf

    def validate_pdfs(self, question_pdf: PyPDF4.PdfFileReader, answer_pdf: PyPDF4.PdfFileReader) -> bool:
        question_text, answer_text = self._parse_cover_page(question_pdf, answer_pdf)
        question_data = self._extract(question_text, "question")
        answer_date = self._extract(answer_text, "answer")
        return question_data["exam_series"] == answer_date["exam_series"]

    def _parse_cover_page(self, question_pdf, answer_pdf):
        question_cover_text = first_page_text(question_pdf)
        answer_cover_text = first_page_text(answer_pdf)
        return question_cover_text, answer_cover_text
    
    def _extract(self, text: str, paper: str) -> dict:
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
        return PDFUtils.convert_to_images(pdf_path)
    
    def _return_pdf_text(self, pdf_path: str) -> str:
        return PDFUtils.extract_text_except_first_page(pdf_path)

    def main(self, question_pdf_path: str, answer_pdf_path: str):
        question_pdf, answer_pdf = self.load_pdfs(question_pdf_path, answer_pdf_path)
        valid = self.validate_pdfs(question_pdf, answer_pdf)
        if valid:
            questions = self._return_pdf_images(question_pdf_path)[1:]
            answers = self._return_pdf_text(answer_pdf_path)
            return questions, answers
        else:
            raise ValueError("Mismatched exam series in question and answer files.")

