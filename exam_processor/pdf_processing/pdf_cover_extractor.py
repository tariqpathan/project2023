import re
from typing import Dict

class PDFCoverPageExtractor:

    def __init__(self, cover_settings: Dict):
        self.cover_settings = cover_settings

    def extract(self, text: str, paper_type: str) -> Dict[str, str|int]:
        """Extracts the exam series from the cover page text."""
        extraction_config = self.cover_settings['regex'][paper_type]
        capture_groups = extraction_config['capture_groups']
        regex = extraction_config['regex']

        match = re.search(regex, text)
        if not match:
            raise ValueError(f"No match found for the given regex. Caused by the exam paper: {paper_type}")

        extracted_data = {}
        for group_name in capture_groups:
            extracted_data[group_name] = match.group(group_name)
        return extracted_data

    def validate_cover_pages_match(self, question_text: str, answer_text: str) -> Dict[str, str|int]:
        """
        Checks if the cover pages from the provided texts match.
        Requires the cover pages in text format.
        Raises a ValueError if the exam series do not match.
        """
        question_data = self.extract(question_text, "question")
        answer_data = self.extract(answer_text, "answer")
        if question_data["exam_series"] != answer_data["exam_series"]:
            raise ValueError("The exam series do not match.")
        return question_data