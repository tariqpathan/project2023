import json
import numpy as np
import pytesseract
import re
from PIL import Image, ImageDraw
from pdfPageToQuestion import ConfigValidator, PageProcessor, QuestionMetadata
from typing import Dict, List, Tuple


class CambridgeScienceConfiguration(ConfigValidator):
    def __init__(self, config_file_loc):
        self.config_file_loc = config_file_loc

    def get_config(self):
        with open(self.config_file_loc, 'r') as f:
            self.config = json.load(f)
            print(self.config)
        # if no config file load defaults
        # if defaults cannot be found, raise an error
        

    def validate_config(self):
        pass

    def calculate_settings(self):
        pass

class QuestionExtractor(PageProcessor):

    def __init__(self, config: Dict):
        self.config = config
        self.binary_threshold = config["binary_threshold"]
        # self.margin
        # self.image_width
        self.image_height = config["image_height"]
        self.padding = config["padding"]
        self.min_question_spaceing = config["min_question_spacing"]
        self.whitespace_threshold = config["whitespace_threshold"]

        self.margin = (self.config["margin_start"], self.config["margin_end"])
        self.image_width = (self.config["question_x_start"], self.config["question_x_end"])


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

    def convert_to_binary_image(self, image: Image.Image) -> Image.Image:
        thresh = self.config["binary_threshold"]
        return image.point(lambda x: 0 if x < thresh else 255, "1")
    
    def create_image_arrays(self, binary_image: Image.Image) -> Dict: #[str: np.ndarray]:
        ystart, yend = 0, self.image_height
        xstart, x_question_end = self.image_width
        x_margin_start, x_margin_end = self.margin
        full_array = np.array(binary_image.crop((xstart, ystart, x_question_end, yend)))
        margin_array = np.array(binary_image.crop((x_margin_start, ystart, x_margin_end, yend)))
        return {"full_array": full_array, "margin_array": margin_array}

    def detect_question_start(self, binary_array, cropped_array, question_spacing=25) -> np.ndarray:
        non_white_rows = np.where(np.any(cropped_array == 0, axis=1))[0]
        nw_row_diffs = np.diff(non_white_rows, prepend=non_white_rows[0])
        non_consecutive_rows = np.where(nw_row_diffs != 1)[0]
        candidate_starts = non_white_rows[non_consecutive_rows]
        question_rows = candidate_starts[np.all(
            binary_array[candidate_starts - question_spacing] == 1, axis=1
            )]
        return question_rows
    
    def get_question_coordinates(self, ques_start_rows: np.ndarray) -> List[Tuple[int, int]]:
        return [(ques_start_rows[i], ques_start_rows[i + 1]) for i in range(len(ques_start_rows) - 1)]
    
    def crop_image(self, image: Image.Image, width: Tuple[int, int], coords: List[Tuple[int, int]]) -> List[Image.Image]:
        (xstart, xend) = width
        return [image.crop((xstart, ystart, xend, yend)) for (ystart, yend) in coords]
    
    def remove_whitespace(self, image: Image.Image) -> Image.Image:
        data = np.array(image)
        min_values = data.min(axis=1)
        non_white_rows = np.where(min_values < self.threshold_value)[0]
        # maybe add a log here?
        top = max(non_white_rows[0] - self.padding, 0)
        bottom = min(non_white_rows[-1] + self.padding, image.height)
        return image.crop((0, top, image.width, bottom))

class QuestionDetail(QuestionMetadata):
    # some of the configurations include: the coordinates for the question block,
    # the mode for pytesseract
    # 
    # also a function to get year, paper, code, subject

    def process(self, image: Image.Image) -> Image.Image:
        pass

    def extract_question_text(
            self, image: Image.Image, coords: Tuple[int, int, int, int], mode: int) -> int:
        q_image = image.crop(coords)
        q_number_string = pytesseract.image_to_string(q_image, config=f'--psm {mode}').strip()
        if q_number_string.isdigit(): return int(q_number_string)
        return -1
    
    def hide_question_number(image: Image.Image, coords: Tuple[int, int, int, int]) -> Image.Image:
        modified_image = image.copy()
        draw = ImageDraw.Draw(modified_image)
        draw.rectangle(coords, fill="white")
        return modified_image

class ExamPaperDetails():

    def get_subjects(self):
        self.subjects = ["BIOLOGY", "CHEMISTRY", "PHYSICS"]
    
    def extract_text(self, image: Image.Image):
        text = pytesseract.image_to_string(image)
        return text
    
    def extract_unit_code(self, text):
        match = re.search(r'([A-Z\s]+)\s(\d{4}/\d{2})', text)
        subject = match.group(1).strip()
        unit_code = match.group(2)
        return (subject, unit_code)

    def extract_date(self, text):
        months = "January|February|March|April|May|June|July|August|September|October|November|December"
        date_pattern = fr'(?P<month1>{months})/(?P<month2>{months})\s+(?P<year>\d{{4}})'
        date_match = re.search(date_pattern, text)

        if date_match:
            date = f"{date_match.group('month1')}/{date_match.group('month2')} {date_match.group('year')}"

        return date if date_match else None



    def process(self, image):
        self.get_subjects()
        text = self.extract_text(image)
        subject = self.extract_unit_code(text)
        date = self.extract_date(text).split()
        date_dict = {"month": date[0], "year": int(date[1])}

        return (subject, date_dict)

if __name__=="__main__":
    i = Image.open('test-page0.jpg')
    t = ExamPaperDetails()
    out = t.process(i)
    print(out)