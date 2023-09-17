import json

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Loads the config file and returns the config as a dictionary."""
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ValueError(f"Config file {self.config_path} not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding the config file. Ensure it's valid JSON.")
    
    def validate(self):
        """Validates the config file. Raises an exception if it's invalid."""
        if 'exam_board' not in self.config:
            raise ValueError("Invalid config file: 'exam_board' key missing.")
        
        
    def get_config(self) -> dict:
        return self.config
