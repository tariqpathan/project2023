"""
constructor
use text extractor
get inherit text extractor and have regex in there
output a list where index value = answer in the form of a tuple or list

either store as separate answer objects or embed within question objects
either way, you'll need the question id to associate the answer with the question

public methods: execute
as there is no images, there is no image processing required
"""

from typing import List
from exam_processor.exam_factory import ExamFactory


class AnswerManager:
    def __init__(self, exam_board: str, config) -> None:
        self.exam_board = exam_board
        self.config = config
        self.text_processor = self._get_text_processor(exam_board)
        self.answer_factory = None
    
    def _get_text_processor(self, exam_board: str) -> RegexTextProcessor:
        """
        Returns an instance of the required OCR processor based on the ocr type.
        """
        if not exam_board: return RegexTextProcessor(self.config[exam_board]["textProcessor"])
        else:
            raise ValueError(f"Unsupported OCR type: {exam_board}")

    def process(self, db_session, text: str, question_ids: List[int]):
        answers = self._extract_answers(text)
        self._create_answers(db_session, answers, question_ids)
        
