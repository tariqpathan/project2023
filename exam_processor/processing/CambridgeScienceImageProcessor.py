from PIL import Image, ImageDraw
from typing import Dict, List, Tuple
import numpy as np
from exam_processor.processing.AbstractImageProcessor import AbstractImageProcessor

class CambridgeScienceImageProcessor(AbstractImageProcessor):
    EXAM_BOARD = "cambridge_science"
    REQUIRED_PARAMS = [
        "binary_threshold",
        "margin_end",
        "footer_height",
        "padding",
        "min_question_spacing",
    ]
    
    def __init__(self, config):
        super().__init__(config)
    
    def _derive_attributes(self, image: Image.Image) -> None:
        """Derive and set specific attributes from the configuration parameters."""
        self._image_height = image.height - self._config["footer_height"]
        self._image_width = image.width
        self._margin = self._config["margin_end"]
        self._padding = self._config["padding"]
        self._min_question_spacing = self._config["min_question_spacing"]
        self._binary_threshold = self._config["binary_threshold"]

    def _validate_attributes(self) -> None:
        """Runs checks for each attribute and raises an exception"""
        checks = {
            self._image_height: {
                'condition': lambda x: x > 0,
                'message': "Height must be positive"
            },
            self._image_width: {
                'condition': lambda x: x > 0,
                'message': "Width must be positive"
            },
            self._margin: {
                'condition': lambda x: x > 0 and x < self._image_width,
                'message': "Margin must be greater than 0 and less than image width"
            },
            self._padding: {
                'condition': lambda x: x >= 0,
                'message': "Padding should be 0 or greater"
            },
            self._min_question_spacing: {
                'condition': lambda x: x >= 0,
                'message': "Question spacing should be 0 or greater"
            },
            self._binary_threshold: {
                'condition': lambda x: 0 < x < 255,
                'message': "Threshold must be between 0 and 255"
            }
        }

        for value, check in checks.items():
            if not check['condition'](value):
                raise ValueError(f"{check['message']}. Current value: {value}")

    def validate(self, image: Image.Image):
        self._derive_attributes(image)
        self._validate_attributes
        

    def process(self, image: Image.Image) -> List[Image.Image]:
        """Converts an image of a page and returns a list of question-images"""
        # Implement the specific steps to process the Cambridge Science image.
        # This can be a sequence of operations using the functions you've provided earlier.
        image = self._remove_vertical_whitespace(image)
        # ... other processing steps
        return [image]

    def post_process(self, image: Image.Image) -> Image.Image:
        """Modifies images after data has been extracted"""
        return image

    def _create_image_arrays(self, binary_image: Image.Image) -> Dict[str, np.ndarray]:
        """Creates a numpy array of the image for quicker process"""
        ystart, yend = 0, self._image_height
        xstart, x_question_end = 0, self._image_width
        x_margin_start, x_margin_end = 0, self._margin
        full_array = np.array(binary_image.crop((xstart, ystart, x_question_end, yend)))
        margin_array = np.array(binary_image.crop((x_margin_start, ystart, x_margin_end, yend)))
        return {"full_array": full_array, "margin_array": margin_array}

    def _detect_question_start(self, binary_array, cropped_array, question_spacing=25) -> np.ndarray:
        """Detects the start of a question and returns as list of y-pixel values"""
        non_white_rows = np.where(np.any(cropped_array == 0, axis=1))[0]
        nw_row_diffs = np.diff(non_white_rows, prepend=non_white_rows[0])
        non_consecutive_rows = np.where(nw_row_diffs != 1)[0]
        candidate_starts = non_white_rows[non_consecutive_rows]
        question_rows = candidate_starts[np.all(
            binary_array[candidate_starts - question_spacing] == 1, axis=1
            )]
        return question_rows

    def _get_question_coordinates(self, ques_start_rows: np.ndarray) -> List[Tuple[int, int]]:
        """Converts start location of question into(start, end) y-coordinates"""
        return [(ques_start_rows[i], ques_start_rows[i + 1]) for i in range(len(ques_start_rows) - 1)]

    def _remove_vertical_whitespace(self, image: Image.Image):
        """Removes vertical whitespace, leaving some padding"""
        data = np.array(image)
        min_values = data.min(axis=1)
        non_white_rows = np.where(min_values < self._binary_threshold)[0]
        top = max(non_white_rows[0] - self._padding, 0)
        bottom = min(non_white_rows[-1] + self._padding, image.height)
        return image.crop((0, top, image.width, bottom))
    
    def _crop_image(self, image: Image.Image, width: Tuple[int, int], coords: List[Tuple[int, int]]) -> List[Image.Image]:
        """Crops images in the y-plane to produce a question-image fragment"""
        (xstart, xend) = width
        return [image.crop((xstart, ystart, xend, yend)) for (ystart, yend) in coords]

    def _overwrite_image(self, image: Image.Image, coords: Tuple[int, int, int, int]) -> Image.Image:
        """Overlays a white box on given image with provided coords"""
        modified_image = image.copy()
        draw = ImageDraw.Draw(modified_image)
        draw.rectangle(coords, fill="white")
        return modified_image