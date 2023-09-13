from typing import List, Dict, Tuple
from PIL import Image
import numpy as np

from exam_processor.processing.QuestionProcessor import QuestionProcessor

class CambridgeScienceQuestionProcessor(QuestionProcessor):

    def validate_config(self):
        pass

    def create_image_arrays(self, binary_image: Image.Image) -> Dict[str, np.ndarray]:
        pass

    def detect_question_start(self, binary_array, cropped_array, question_spacing=25) -> np.ndarray:
        pass

    def get_question_coordinates(self, ques_start_rows: np.ndarray) -> List[Tuple[int, int]]:
        pass

    def create_question(self, ):
        pass

