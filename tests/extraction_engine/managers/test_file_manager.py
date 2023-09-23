# Test for file_manager.py
import pytest
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
        FileManager._to_path(None)   # type: ignore
        FileManager._to_path('incorrect')    

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
#TODO: fix this test
def test_resolve_path(monkeypatch):
    monkeypatch.setenv("TEST_ENV_VAR", "/env/var/path")
    path = FileManager.resolve_path("file.txt", "TEST_ENV_VAR")
    assert path == Path("/env/var/path/file.txt")

    path = FileManager.resolve_path("file.txt", "NON_EXISTENT_ENV_VAR")
    assert path == FileManager.root_path / "file.txt"

# This is for running the tests if you're not using a separate test runner
if __name__ == "__main__":
    pytest.main([__file__])