# Test for file_manager.py
import pytest
import json
from pathlib import Path
from extraction_engine.managers.file_manager import FileManager


def test_set_root_path():
    FileManager.set_root_path("/new/root")
    assert FileManager.root_path == Path("/new/root")

def test_to_path():
    path = FileManager._to_path("/some/path")
    assert isinstance(path, Path)
    assert path == Path("/some/path")

    with pytest.raises(ValueError):
        FileManager._to_path(12)

def test_construct_path():
    path = FileManager.construct_path("file.txt")
    assert path == FileManager.root_path / "file.txt"

    path = FileManager.construct_path("file.txt", "/some/base")
    assert path == Path("/some/base/file.txt")

def test_is_valid_file(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    assert FileManager.is_valid_file(str(file_path)) is True

    non_existent_path = tmp_path / "non_existent.txt"
    assert FileManager.is_valid_file(str(non_existent_path)) is False

def test_load_paths(mocker):
    mock_json_data = json.dumps({"some_path": "/some/path"})
    mocker.patch('builtins.open', mocker.mock_open(read_data=mock_json_data))
    mocker.patch('json.load', json.load)

    FileManager._load_paths()
    assert FileManager._paths_cache == {"some_path": "/some/path"}

def test_get_cached_path():
    FileManager._paths_cache = {"some_path": "/some/path"}
    path = FileManager._get_cached_path("some_path")
    assert path == "/some/path"

def test_get_filepaths(mocker):
    mocker.patch.object(FileManager, '_get_cached_path', return_value="/some/path")
    mocker.patch.object(FileManager, 'construct_path', return_value=Path("/root/some/path"))

    path = FileManager.get_filepaths("some_path")
    assert path == Path("/root/some/path")

def test_get_env_paths_or_default(mocker, monkeypatch):
    mocker.patch.object(FileManager, '_load_paths')
    monkeypatch.setenv("ENV_PATH", "/env/path")

    FileManager.get_env_paths_or_default("ENV_PATH")

    FileManager._load_paths.assert_called_once()
    assert FileManager.paths_location == Path("/env/path")

if __name__ == "__main__":
    pytest.main([__file__])