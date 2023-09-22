# Test for config_manager.py

import unittest
from unittest.mock import mock_open, patch
from extraction_engine.managers.config_manager import ConfigManager

class ConfigManagerTest(unittest.TestCase):
    def setUp(self):
        # Sample valid JSON for mocking purposes
        self.mock_data = '{"sample_format": {"key": "value"}}'

    def test_load_valid_config(self):
        with patch("builtins.open", mock_open(read_data=self.mock_data)):
            cm = ConfigManager()
            config = cm._load_config("config")
            self.assertIn("sample_format", config)

    def test_load_invalid_config(self):
        with self.assertRaises(ValueError):
            cm = ConfigManager()
            cm._load_config("nonexistent_config")

    def test_get_config(self):
        with patch("builtins.open", mock_open(read_data=self.mock_data)):
            cm = ConfigManager()
            board_config = cm.get_config("config", "sample_format")
            self.assertIn("key", board_config)

if __name__ == '__main__':
    unittest.main()
