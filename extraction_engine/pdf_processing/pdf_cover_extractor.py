import re
from typing import Dict
import logging

import yaml

logger = logging.getLogger(__name__)

class PDFCoverPageExtractor:

    def __init__(self, cover_settings: Dict):
        logging.debug("PDFCoverPageExtractor.__init__ called")
        self.cover_settings = cover_settings

    def extract(self, text: str, paper_type: str) -> Dict[str, str|int]:
        """Extracts the exam series from the cover page text."""
        extraction_config = self.cover_settings['regex'][paper_type]
        capture_groups = extraction_config['capture_groups']
        regex = extraction_config['regex']
        if not regex:
            raise KeyError(f"Regex not found for the given exam paper: {paper_type}")

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
        logging.debug(f"question_data: {question_data}")
        answer_data = self.extract(answer_text, "answer")
        if question_data["exam_series"] != answer_data["exam_series"]:
            raise ValueError("The exam series do not match.")
        return question_data
    
if __name__=="__main__":
    with open('./config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    settings = config['coverpage_settings']['cambridge_science']['question']
    with open('./tests/test_question_cover.txt', 'r') as f:
        text = f.read()
    
    regexes = {
        "subject": r"\b([A-Z]{6,})\b",
        "unit_code": r"\b(\d{4})\/\d{2}\b",
        "component_code": r"\b\d{4}\/(\d{2})\b",
        "Month": r"\b([A-Z]{1}[a-z]+)\/?[A-Z]{1}[a-z]+\s20\d{2}\b",
        "Year": r"\bUCLES\s+(\d{4})\b",
        "Type": r"(MARK SCHEME)"
    }
    extracted_data = {}
    for group_name, regex in regexes.items():
        match = re.search(regex, text)
        if match:
            extracted_data[group_name] = match.group(1)
        else:
            extracted_data[group_name] = None
    print(extracted_data)