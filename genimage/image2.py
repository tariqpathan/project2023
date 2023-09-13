"""
imagegenerator.py is designed to convert a pdf and convert it to a series of jpegs
This is a test version.
Some of the changes that need to be implemented are:
1) Apply a proper naming structure to the files
2) Print out a success/update message when conversion is complete
3) Think about how this hooks into the whole software structure
4) Once the process is complete - how would cleanup looklike
5) What about recovery/backup options in case something goes wrong?
"""
import os
from pathlib import Path
import fitz

dir_path = Path(__file__).parent.parent
print(dir_path)
file_location = "test.pdf"
pdf_path = os.path.join(dir_path, file_location)
print(pdf_path)
try:
    pdf = fitz.open(pdf_path)
except Exception as exc:
    print(exc)
    quit()
print(type(pdf))
for page in range(pdf.page_count):
    current_page = pdf[page]

    pix = current_page.get_pixmap()
    print(f'h: {pix.height}, w: {pix.width}')
    name = f'test-page{page}.jpg'
    pix.save(name, "JPEG")
