import os
import PyPDF4
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

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
    image = Image.open('test-ans-page0.jpg')
    return image.width, image.height

def convert_test():
    pdf_images = convert_from_path(pdf_path)
    for i, image in enumerate(pdf_images):
        image.save(f'test-ans-page{i}.jpg', 'JPEG')

def print_image_details():
    w, h = get_pdf_details()
    print(f'width: {w}, height: {h}')

    iw, ih = get_image_details()
    print(f'image-width: {iw}, image-height: {ih}')

    factorh = float(ih/h)
    factorw = float(iw/w)
    print(factorh, factorw)


if __name__ == "__main__":
    convert_test()
