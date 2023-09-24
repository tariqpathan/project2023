import re
from typing import Dict, Union
import logging

import yaml

logger = logging.getLogger(__name__)

class PDFCoverPageExtractor:
    KEY_NAME_FOR_YAML_CONFIG = "regexes"

    def __init__(self, cover_settings: Dict):
        self.cover_settings = cover_settings

    def extract(self, text: str) -> Dict[str, Union[str, int, bool]]:
        """Extracts the exam series from the cover page text."""
        extraction_config = self.cover_settings[self.KEY_NAME_FOR_YAML_CONFIG]
        # logging.debug(f"extraction_config: {extraction_config}")
        if not extraction_config:
            raise KeyError(f"Regex not found for the given exam paper: {self.cover_settings.keys()}")

        extracted_data = {}
        for group_name, regex in extraction_config.items():
            match = re.search(regex, text)
            if match:
                extracted_data[group_name] = True if group_name == "answer" else match.group(1)
            else:
                extracted_data[group_name] = None
        return extracted_data

    def validate_cover_pages_match(self, question_text: str, answer_text: str) -> Dict[str, str|int]:
        """
        Checks if the cover pages from the provided texts match.
        Requires the cover pages in text format.
        Raises a ValueError if the exam series do not match.
        """
        keys_to_compare = ['unit_code', 'component_code', 'month', 'year', 'subject']
        question_data = self.extract(question_text)
        answer_data = self.extract(answer_text)
        logging.debug(f"question_data: {question_data}\nanswer_data: {answer_data}")

        for key in keys_to_compare:
            if question_data.get(key) != answer_data.get(key):
                raise ValueError(f"The cover pages do not match for {key}.\n" \
                    f"They are: {question_data.get(key)}, and {answer_data.get(key)}")
        if question_data.get('answer') != None and not answer_data.get('answer'):
            raise ValueError(f"Mark scheme not correctly identified. Check file names.")
        return question_data