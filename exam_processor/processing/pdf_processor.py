import PyPDF4
import pdf2image as p2i
#TODO: Delete file

def open_pdf(file_path: str):
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
    except PyPDF4.utils.PdfReadError:
        raise PyPDF4.utils.PdfReadError(f"Could not read the PDF file '{file_path}'. It might be corrupted or unsupported.")
    except PyPDF4.utils.PdfPasswordError:
        raise PyPDF4.utils.PdfPasswordError(f"The PDF file '{file_path}' is encrypted and requires a password.")
    except IOError:
        raise IOError(f"An I/O error occurred while accessing '{file_path}'.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred with file '{file_path}': {e}")

def close_pdf(pdf: PyPDF4.PdfFileReader):
    """Closes the pdf reader object"""
    pdf.stream.close()
    print('PDF file closed')

def first_page_text(pdf: PyPDF4.PdfFileReader):
    """Converts the first page of a pdf. Requires PdfFileReader object"""
    try: 
        page = pdf.getPage(0)
        return page.extractText()
    except Exception as e:
        raise Exception(f'The first page could not be accessed') # custom exception?

def convert_to_images(filepath):
    """Converts a pdf to images and returns as a list of images"""
    try:
        return p2i.convert_from_path(filepath)
    except Exception as e:
        raise Exception(f'Error in converting the PDF to images: {str(e)}')
