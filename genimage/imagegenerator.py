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
    
