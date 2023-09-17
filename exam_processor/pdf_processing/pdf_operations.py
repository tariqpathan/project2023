from PyPDF4 import utils as PyPDF4_utils
import PyPDF4
from pdf2image import pdf2image

class PDFUtils:

    @staticmethod
    def load_pdf(file_path: str) -> PyPDF4.PdfFileReader:
        """Open the provided PDF file and return the pdf reader object."""
        try:
            f = open(file_path, 'rb')
            pdf_reader = PyPDF4.PdfFileReader(f)
            return pdf_reader
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except PermissionError:
            raise PermissionError(f"No permission to read '{file_path}'.")
        except IsADirectoryError:
            raise IsADirectoryError(f"'{file_path}' is a directory, not a file.")
        except PyPDF4_utils.PdfReadError:
            raise PyPDF4_utils.PdfReadError(f"Could not read the PDF file '{file_path}'. It might be corrupted or unsupported.")
        except IOError:
            raise IOError(f"An I/O error occurred while accessing '{file_path}'.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred with file '{file_path}': {e}")

    @staticmethod
    def close_pdf(pdf: PyPDF4.PdfFileReader) -> None:
        """Closes the pdf reader object"""
        pdf.stream.close()
        print('PDF file closed')

    @staticmethod
    def first_page_text(pdf: PyPDF4.PdfFileReader) -> str:
        """Extracts text from the first page of a PDF. Requires PdfFileReader object."""
        try:
            page = pdf.getPage(0)
            return page.extractText()
        except Exception:
            raise Exception(f'The first page could not be accessed')  # Add more details to the exception if necessary

    @staticmethod
    def convert_to_images(filepath: str) -> list:
        """Converts a pdf to images and returns them as a list of images."""
        try:
            return pdf2image.convert_from_path(filepath)
        except Exception as e:
            raise Exception(f'Error in converting the PDF to images: {str(e)}')

    @staticmethod    
    def extract_text_except_first_page(filepath: str) -> str:
        """Extracts text from a PDF, excluding the first page."""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF4.PdfFileReader(file)
            num_pages = pdf_reader.numPages
            text = ""
            for page_num in range(1, num_pages):
                text += pdf_reader.getPage(page_num).extractText()
        return text
