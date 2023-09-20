import os
import json
from file_manager import FileManager

class ConfigManager:

    BASE_PATH = FileManager.get_root_path()
    CONFIG_BASE_PATH = os.path.join(BASE_PATH, "config")

    _instance = None  # The single instance of ConfigManager

    def __new__(cls):
        # Ensure only one instance of ConfigManager is created
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.CONFIG_PATHS = {
            "config": self._resolve_path('config.json', 'CONFIG_PATH'),
            "coverpage_settings": self._resolve_path('coverpage_settings.json', 'COVERPAGE_SETTINGS_PATH')
        }

    @staticmethod
    def _resolve_path(filename: str, env_var: str) -> str:
        default_path = FileManager.construct_path(filename, base_path=ConfigManager.CONFIG_BASE_PATH)
        return os.environ.get(env_var, default_path)

    def _load_config(self, config_type: str):
        """Loads the config file based on its type and returns the config as a dictionary."""
        path = self.CONFIG_PATHS.get(config_type)
        if not path:
            raise ValueError(f"Unknown config type: {config_type}")

        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ValueError(f"Config file {path} not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding the config file. Ensure it's valid JSON.")

    def get_config(self, config_type: str, exam_format: str) -> dict:
        """Returns the configuration for a specific exam board."""
        config = self._load_config(config_type)
        board_config = config.get(exam_format)

        if not board_config:
            raise ValueError(f"No configuration found for exam board: {exam_format}")

        return board_config
