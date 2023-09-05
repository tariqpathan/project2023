import numpy as np
import pytesseract
from PIL import Image, ImageDraw
from pdfPageToQuestion import PageProcessor
from typing import List, Tuple

class QuestionExtractor(PageProcessor):

    def __init__(self):
        self.threshold_value = 0
        self.

    def process(self, image: Image.Image) -> List[Image.Image]:
        grayscale = self.convert_to_grayscale_image(image)
        binary = self.convert_to_binary_image(grayscale)
        # need to crop, create binary and cropped arrays
        # call detect question start
        # call get coordinates using start points
        # call crop images using coordinates
        # call remove whitespace

    def convert_to_grayscale_image(self, image:Image.Image) -> Image.Image:
        return image.convert('L')

    def convert_to_binary_image(self, image: Image.Image, thresh:int) -> Image.Image:
        return image.point(lambda x: 0 if x < thresh else 255, "1")
    
    def get_footer_height(self) -> int:
            """Removes the footer from image processing operations"""
            return 120
    
    def calculate_image_height(self) -> int:
        return 0
    
    def set_margin_width(self) -> Tuple[int, int]:
        return (0, 0)
    
    def set_question_width(self) -> Tuple[int, int]:
        return (0, 0)

    def detect_question_start(self, binary_array, cropped_array, question_spacing=25) -> np.ndarray:
        non_white_rows = np.where(np.any(cropped_array == 0, axis=1))[0]
        nw_row_diffs = np.diff(non_white_rows, prepend=non_white_rows[0])
        non_consecutive_rows = np.where(nw_row_diffs != 1)[0]
        candidate_starts = non_white_rows[non_consecutive_rows]
        question_rows = candidate_starts[np.all(
            binary_array[candidate_starts - question_spacing] == 1, axis=1
            )]
        return question_rows
    
    def get_question_coordinates(self, ques_start_rows: np.ndarray, padding=50) -> List[Tuple[int, int]]:
        return [(ques_start_rows[i] - padding, ques_start_rows[i + 1] - padding) for i in range(len(ques_start_rows) - 1)]
    
    def crop_image(self, image: Image.Image, width: Tuple[int, int], coords: List[Tuple[int, int]]) -> List[Image.Image]:
        (xstart, xend) = width
        return [image.crop((xstart, ystart, xend, yend)) for (ystart, yend) in coords]
    
    def remove_whitespace(self, image: Image.Image) -> Image.Image:
        data = np.array(image)
        min_values = data.min(axis=1)
        non_white_rows = np.where(min_values < self.threshold_value)[0]
        if non_white_rows.size == 0:
            print("No content detected in the image.")
            return
        
        top = max(non_white_rows[0] - self.padding, 0)
        bottom = min(non_white_rows[-1] + self.padding, image.height)
        return image.crop((0, top, image.width, bottom))

class QuestionDetail():
    # some of the configurations include: the coordinates for the question block,
    # the mode for pytesseract
    # 
    # also a function to get year, paper, code, subject

    def process(self, image: Image.Image) -> Image.Image:
        pass

    def extract_question_text(
            self, image: Image.Image, coords: Tuple[int, int, int, int], mode: int) -> str:
        q_image = image.crop(coords)
        q_number_string = pytesseract.image_to_string(q_image, config=f'--psm {mode}').strip()
        return ''
    
    def hide_question_number(image: Image.Image, coords: Tuple[int, int, int, int]) -> Image.Image:
        modified_image = image.copy()
        draw = ImageDraw.Draw(modified_image)
        draw.rectangle(coords, fill="white")
        return modified_image
