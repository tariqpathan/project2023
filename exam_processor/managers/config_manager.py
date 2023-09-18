import os
import json

class ConfigManager:
    # Default paths and potential environment variables.
    CONFIG_PATHS = {
        "config": os.environ.get('CONFIG_PATH', 'config/config.json'),
        "coverpage_settings": os.environ.get('COVERPAGE_SETTINGS_PATH', 'config/coverpage_settings.json')
    }

    def __init__(self):
        pass

    @classmethod
    def _load_config(cls, config_type):
        """Loads the config file based on its type and returns the config as a dictionary."""
        path = cls.CONFIG_PATHS.get(config_type)
        if not path:
            raise ValueError(f"Unknown config type: {config_type}")

        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ValueError(f"Config file {path} not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding the config file. Ensure it's valid JSON.")

    def get_config(self, config_type, exam_board) -> dict:
        """Returns the configuration for a specific exam board."""
        config = self._load_config(config_type)
        board_config = config.get(exam_board)

        if not board_config:
            raise ValueError(f"No configuration found for exam board: {exam_board}")
        
        return board_config

