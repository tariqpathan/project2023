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
import PyPDF4
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import re

dir_path = Path(__file__).parent.parent
file_location = "test-answers.pdf"
pdf_path = os.path.join(dir_path, file_location)
print(pdf_path)

def get_pdf_details():
    with open(pdf_path, "rb") as f:
        reader = PyPDF4.PdfFileReader(f)
        page = reader.getPage(0)  # get the first page
        media_box = page.mediaBox
        width, height = media_box.upperRight
        return width, height

def get_image_details():
    image = Image.open('test-page0.jpg')
    return image.width, image.height

def convert_test():
    pdf_images = convert_from_path(pdf_path)
    for i, image in enumerate(pdf_images):
        image.save(f'test-answers-page{i}.jpg', 'JPEG')

def process_details():
    w, h = get_pdf_details()
    print(f'width: {w}, height: {h}')

    iw, ih = get_image_details()
    print(f'image-width: {iw}, image-height: {ih}')

    factorh = float(ih/h)
    factorw = float(iw/w)
    print(factorh, factorw)

def get_text_from_answers():
    with open(pdf_path, "rb") as f:
        reader = PyPDF4.PdfFileReader(f)
        print(f'No. of pages: {reader.getNumPages()}')
        first_page = reader.getPage(0).extractText()
        answer_page_one(first_page)
        page_content = reader.getPage(1).extractText()

    return page_content

def answer_page_one(text):
    code_pattern = re.compile(r'(\d{4})/(\d{2})')
    code_match = code_pattern.search(text)
    subject_code, component_code = code_match.groups() if code_match else (None, None)
    print(subject_code, component_code)

def get_answer_details(text):
    options = set(['A', 'B', 'C', 'D'])
    answers = {}
    lines = [t.strip() for t in text.split("\n")]
    i = 0
    while i < len(lines) - 2:  # Ensuring we don't overrun the list
        line = lines[i]    
        if line.isdigit() and line.isdigit() and lines[i+1] in options:
            num = int(line)
            answers[num] = lines[i+1]
        i += 1
    return answers
        
def process_answers_pdf():
    text = get_text_from_answers()
    res = get_answer_details(text)
    print(res)

if __name__ == "__main__":
    process_answers_pdf()