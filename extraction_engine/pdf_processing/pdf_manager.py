from typing import Any, Dict
import PyPDF4
from extraction_engine.managers.config_manager import ConfigManager
from extraction_engine.pdf_processing.pdf_cover_extractor import PDFCoverPageExtractor
from extraction_engine.pdf_processing.pdf_utils import PDFUtils
import logging

logger = logging.getLogger(__name__)
class PDFManager:
    def __init__(self, exam_format: str):
        self.CONFIG_TYPE = "coverpage_settings"
        self.exam_format = exam_format
        self.cover_settings = self._get_cover_settings()
        self.cover_page_extractor = PDFCoverPageExtractor(self.cover_settings)

    def _get_cover_settings(self) -> dict:
        return ConfigManager().get_config(config_type=self.CONFIG_TYPE, exam_format=self.exam_format)
        
    def _return_pdf_images(self, pdf_path: str) -> list:
        """Returns a list of images from a PDF file, excluding the cover page."""
        return PDFUtils.convert_to_images(pdf_path)
    
    def _return_pdf_text(self, pdf_path: str) -> str:
        """Returns all the text from a PDF file, excluding the cover page."""
        return PDFUtils.extract_text_except_first_page(pdf_path)

    def _get_exam_cover_details(self, pdf: PyPDF4.PdfFileReader) -> Dict[str, str|int]:
        text = PDFUtils.first_page_text(pdf)
        return self.cover_page_extractor.extract(text) # cover details come from question paper

    def extract_pdf_data(self, question_pdf_path: str, answer_pdf_path: str) -> Dict[str, Any]:
        """
        Extracts cover details as a dict, images of the question paper as a list, 
        and the answer text as a string. Returns as a tuple of three elements.
        """
        question_pdf = None
        answer_pdf = None
        try:
            question_pdf = PDFUtils.load_pdf(question_pdf_path)
            answer_pdf = PDFUtils.load_pdf(answer_pdf_path)
            q_cover_text = PDFUtils.first_page_text(question_pdf)
            a_cover_text = PDFUtils.first_page_text(answer_pdf)
            cover_details = self.cover_page_extractor.validate_cover_pages_match(q_cover_text, a_cover_text)
            questions = self._return_pdf_images(question_pdf_path)[1:]
            answers = self._return_pdf_text(answer_pdf_path)
            return {"cover_details": cover_details,
                    "questions": questions,
                     "answers": answers}
        
        except Exception as e:
            raise Exception(f"Error with input pdf files: {e}" \
                f"\nInput: Question PDF: {question_pdf_path}, Answer PDF: {answer_pdf_path}")
        finally:
            if question_pdf: PDFUtils.close_pdf(question_pdf)
            if answer_pdf: PDFUtils.close_pdf(answer_pdf)
    