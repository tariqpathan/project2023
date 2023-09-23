import re
from typing import Dict

from extraction_engine.processing.AbstractAnswerProcessor import AbstractAnswerProcessor

class CambridgeScienceAnswerProcessor(AbstractAnswerProcessor):
    EXAM_FORMAT = "cambridge_science"
    
    def _extract_answers(self, text: str) -> Dict[int, str]:
        """
        In the case of Cambridge Science, the answers are in the form of a table
        and are single letters. This method extracts the answers from the text and
        returns them as a dictionary.
        """
        options = set(['A', 'B', 'C', 'D'])
        answers = {}
        lines = [t.strip() for t in text.split("\n")]
        i = 0
        while i < len(lines) - 2:  # Ensuring we don't overrun the list
            line = lines[i]    
            if line.isdigit() and lines[i+1] in options:
                num = int(line)
                answers[num] = lines[i+1]
            i += 1
        return answers
    
    def process(self, text: str) -> Dict[int, str]:
        """
        Extracts the answers from the text and returns them as a list where index is qnum.
        """
        return self._extract_answers(text)