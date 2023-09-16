import json

class ExamBoardConfig:
    CONFIG_PATH = 'config.json'

    def __init__(self, exam_board_name):
        self.exam_board_name = exam_board_name
        self.raw_config = self.load_config()
        self.validate()

    def load_config(self):
        """Load the raw configuration from the JSON file."""
        with open(ExamBoardConfig.CONFIG_PATH, 'r') as file:
            all_configs = json.load(file)
            return all_configs.get(self.exam_board_name)

    def validate(self):
        """Validate the raw configuration."""
        if not self.raw_config:
            raise ValueError(f"Configuration for {self.exam_board_name} is empty.")

        # Validate imageProcessor configuration
        self.validate_section('imageProcessor', [
            'binary_threshold', 'margin_start', 'margin_end',
            'footer_height', 'padding', 'min_question_spacing',
            'whitespace_threshold'
        ])

        # Validate OCRProcessor configuration
        self.validate_section('OCRProcessor', [
            'question_x_start', 'question_y_start', 'question_x_end',
            'question_y_end', 'tesseract_psm_mode'
        ])

    def validate_section(self, section_name, expected_keys):
        """Validate a section of the configuration."""
        section = self.raw_config.get(section_name, {})

        if not section:
            raise ValueError(f"'{section_name}' section is missing from the configuration.")

        for key in expected_keys:
            value = section.get(key)
            
            if value is None:
                raise ValueError(f"'{key}' is missing from the '{section_name}' configuration.")
            
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"'{key}' in '{section_name}' should be a non-negative integer. Got {value}.")

    @staticmethod
    def available_exam_boards():
        """Return a list of available exam boards from the configuration."""
        with open(ExamBoardConfig.CONFIG_PATH, 'r') as file:
            all_configs = json.load(file)
            return list(all_configs.keys())
