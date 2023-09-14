from PIL import Image, ImageDraw
from typing import Dict, List, Tuple
import numpy as np
import AbstractImageProcessor

class CambridgeScienceImageProcessor(AbstractImageProcessor):
    
    def validate_config(self, image: Image.Image):
        """Validate ImageProcessor-specific configuration"""
        pass

    def process(self, image: Image.Image) -> Image.Image:
        """Converts an image of a page and returns a list of question-images"""
        # Implement the specific steps to process the Cambridge Science image.
        # This can be a sequence of operations using the functions you've provided earlier.
        image = self.remove_vertical_whitespace(image)
        # ... other processing steps
        return image

    def post_process(self, image: Image.Image) -> Image.Image:
        """Modifies images after data has been extracted"""
        pass

    def _create_image_arrays(self, binary_image: Image.Image) -> Dict: #[str: np.ndarray]:
        """Creates a numpy array of the image for quicker process"""
        ystart, yend = 0, self._image_height
        xstart, x_question_end = self._image_width
        x_margin_start, x_margin_end = self._margin
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
        non_white_rows = np.where(min_values < self._threshold)[0]
        top = max(non_white_rows[0] - self._padding, 0)
        bottom = min(non_white_rows[-1] + self._padding, image.height)
        return image.crop((0, top, image.width, bottom))
    
    def _crop_image(self, image: Image.Image, width: Tuple[int, int], coords: List[Tuple[int, int]]) -> List[Image.Image]:
        """Crops images in the y-plane to produce a question-image fragment"""
        (xstart, xend) = width
        return [image.crop((xstart, ystart, xend, yend)) for (ystart, yend) in coords]

    def _overwrite_image(image: Image.Image, coords: Tuple[int, int, int, int]) -> Image.Image:
        """Overlays a white box on given image with provided coords"""
        modified_image = image.copy()
        draw = ImageDraw.Draw(modified_image)
        draw.rectangle(coords, fill="white")
        return modified_image