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
from pdf2image import convert_from_path

dir_path = Path(__file__).parent.parent
file_location = "test.pdf"
pdf_path = os.path.join(dir_path, file_location)

print(pdf_path)


pdf_images = convert_from_path(pdf_path)

for i, image in enumerate(pdf_images):
    image.save(f'test-page{i}.jpg', 'JPEG')
    
