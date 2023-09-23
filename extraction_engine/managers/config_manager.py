import os
import json
from pathlib import Path
from extraction_engine.managers.file_manager import FileManager

class ConfigManager:
    """
    Manages the configuration files for the application.
    CONFIG_BASE_PATH: Name of the directory where the config files are stored.
    Default directory structure: root_path/config
    """
    CONFIG_BASE_PATH = FileManager.construct_path("config")
    _instance = None  # The single instance of ConfigManager
    paths = {}  # Class-level attribute for paths

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls.paths = cls._load_paths()
            cls._initialize_config_paths()
        return cls._instance

    @staticmethod
    def _load_paths():
        path = FileManager.construct_path('/paths.json')
        try:
            with path.open(encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ValueError("paths.json not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding paths.json. Ensure it's valid JSON.")

    @classmethod
    def _get_path_from_env_or_default(cls, filename: str, env_var: str) -> Path:
        """
        Resolves the path for a given filename, using the environment variable if it exists.
        Expected environment variables: CONFIG_PATH, COVERPAGE_SETTINGS_PATH
        """
        default_path = FileManager.construct_path(filename)
        return Path(os.environ.get(env_var, default_path))

    def __init__(self):
        if self._instance:
            return  # Avoid reinitializing if an instance already exists

    @classmethod
    def _initialize_config_paths(cls):
        cls._CONFIG_PATHS = {}
        for key, name in cls.paths.items():
            cls._CONFIG_PATHS[key] = FileManager.construct_path(CONFIG_BASE_PATH, name)

    def _load_config(self, config_type: str):
        """Loads the config file based on its type and returns the config as a dictionary."""
        path = self._CONFIG_PATHS.get(config_type)
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