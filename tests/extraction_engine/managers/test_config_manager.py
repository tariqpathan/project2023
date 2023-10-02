import pytest
from pathlib import Path

import yaml

from extraction_engine.managers.config_manager import ConfigManager  # Adjust the import to your package structure

# Mock data for testing
mock_config_data = {
    'exam_formats': {
        'format1': {'key1': 'value1', 'key2': 'value2'},
        'format2': {'key3': 'value3', 'key4': 'value4'}
    },
    'other_config': {'key5': 'value5'}
}


def test_get_file_path(monkeypatch):
    # Mock FileManager.get_filepaths to return a specific path
    monkeypatch.setattr('extraction_engine.managers.file_manager.FileManager.get_filepaths', lambda x: Path('/mock/path'))
    assert ConfigManager._get_file_path() == Path('/mock/path')


def test_load_config(monkeypatch, tmp_path):
    # Create a temporary config file with mock data
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(mock_config_data))

    # Test the _load_config method
    cm = ConfigManager()
    loaded_config = cm._load_config(config_file)
    assert loaded_config == mock_config_data




def test_get_all_exam_formats(monkeypatch, tmp_path):
    # Create a temporary config file with mock data
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(mock_config_data))

    # Mock _get_file_path to return the path to the temporary config file
    monkeypatch.setattr('extraction_engine.managers.config_manager.ConfigManager._get_file_path', lambda x: config_file)

    # Test the get_all_exam_formats method
    exam_formats = ConfigManager.get_all_exam_formats()
    assert exam_formats == ['format1', 'format2']
