from typing import Dict, Optional
import yaml
from pathlib import Path
from .file_manager import FileManager
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            config_path = cls._get_file_path()
            # logging.debug(f"ConfigManager.__new__ config_path: {config_path}")
            cls._instance._load_config(config_path)
        return cls._instance

    @classmethod
    def _get_file_path(cls, filepath: str='config') -> Path:
        return FileManager.get_filepaths(filepath)

    def _load_config(self, file: Path) -> Dict:
        with open(file, 'r') as config_file:
            self._config = yaml.safe_load(config_file)
        # logging.debug(f"self._config in ConfigManager: {self._config}")
        return self._config

    @classmethod
    def get_config(cls, exam_format, config_type=None):
        if not cls._instance:
            cls._instance = cls()
        if cls._instance._config is None:
            raise ValueError("Configuration has not been loaded.")
        if config_type:
            return cls._instance._config.get(config_type, {}).get(exam_format)
        return cls._instance._config.get(exam_format)
    
    @classmethod
    def get_all_exam_formats(cls):
        if not cls._instance:
            cls._instance = cls()
        if cls._instance._config is None:
            raise ValueError("Configuration has not been loaded.")
        return list(cls._instance._config.get('exam_formats', {}).keys())
