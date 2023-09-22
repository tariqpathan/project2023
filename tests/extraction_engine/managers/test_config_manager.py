# Test for config_manager.py
import shutil
import pytest
from extraction_engine.managers.config_manager import ConfigManager
from extraction_engine.managers.file_manager import FileManager
import json
from pathlib import Path
import os

# Fixture to set up the paths.json and other required config files
@pytest.fixture()
def setup_files(tmp_path):
    paths_json = {
        "config": "config/config.json",
        "coverpage_settings": "config/coverpage_settings.json"
    }
    config_data = {
        "exam_board": {
            "setting1": "value1",
            "setting2": "value2"
        }
    }
    FileManager.set_root_path(tmp_path)
    config_dir = tmp_path / 'config'
    config_dir.mkdir()
    (config_dir / 'paths.json').write_text(json.dumps(paths_json))
    (config_dir / 'config.json').write_text(json.dumps(config_data))
    (config_dir / 'coverpage_settings.json').write_text(json.dumps(config_data))
    yield
    # teardown (if necessary)
    # shutil.rmtree(tmp_path)

def test_load_paths(setup_files):
    paths = ConfigManager._load_paths()
    assert paths == {
        "config": "config/config.json",
        "coverpage_settings": "config/coverpage_settings.json"
    }

def test_get_path_from_env_or_default(setup_files, monkeypatch):
    monkeypatch.setenv("CONFIG_PATH", str(Path("alternate/config.json")))
    path = ConfigManager._get_path_from_env_or_default("config/config.json", "CONFIG_PATH")
    assert path == Path("alternate/config.json")

def test_load_config(setup_files):
    cm = ConfigManager.get_instance()
    config = cm._load_config("config")
    assert config == {
        "exam_board": {
            "setting1": "value1",
            "setting2": "value2"
        }
    }

def test_get_config(setup_files):
    cm = ConfigManager.get_instance()
    config = cm.get_config("config", "exam_board")
    assert config == {
        "setting1": "value1",
        "setting2": "value2"
    }

def test_invalid_json(tmpdir, setup_files):
    # setup_files(tmpdir)

    # Create an invalid JSON file
    with open(tmpdir / "invalidconfig.json", "w") as f:
        f.write("invalid json")

    with pytest.raises(Exception) as exc_info:
        ConfigManager.get_instance().get_config("invalidconfig", "exam_board")
    assert "Error decoding the config file. Ensure it's valid JSON." in str(exc_info.value)

def test_missing_json_keys(tmpdir, setup_files):
    # setup_files(tmpdir)

    # Create a JSON file missing necessary keys
    with open(tmpdir / "config.json", "w") as f:
        json.dump({}, f)

    with pytest.raises(ValueError) as exc_info:
        ConfigManager.get_instance().get_config("config", "some_format")
    # assert "No configuration found for exam board: some_format" in str(exc_info.value)

def test_missing_files(tmpdir, setup_files):
    # setup_files(tmpdir)

    # Delete the paths.json file
    os.remove(tmpdir / "paths.json")

    with pytest.raises(ValueError) as exc_info:
        ConfigManager.get_instance()
    assert "paths.json not found." in str(exc_info.value)

def test_unknown_config_type(tmpdir, setup_files):
    # setup_files(tmpdir)

    with pytest.raises(ValueError) as exc_info:
        ConfigManager.get_instance().get_config("unknown", "some_format")
    assert "Unknown config type: unknown" in str(exc_info.value)

def test_nonexistent_file_path(tmpdir, setup_files):
    # setup_files(tmpdir)

    with pytest.raises(FileNotFoundError) as exc_info:
        FileManager.construct_path("nonexistent_file.txt")
    assert "File or directory not found:" in str(exc_info.value)

def test_invalid_root_path(setup_files):
    with pytest.raises(ValueError) as exc_info:
        FileManager.set_root_path('invalid')
    assert "Failed to convert string to Path:" in str(exc_info.value)
