import pytest
from PIL import Image

from extraction_engine.managers.file_manager import FileManager
from extraction_engine.managers.image_file_handler import ImageFileHandler  # Replace with the actual import


# Mock FileManager functions
@pytest.fixture
def mock_file_manager(mocker):
    mocker.patch.object(FileManager, 'get_filepaths', return_value="/base_path")
    mocker.patch.object(FileManager, 'construct_path', return_value="/base_path/image.jpg")


# Mock Image.save
@pytest.fixture
def mock_image_save(mocker):
    mocker.patch.object(Image.Image, 'save')


# Test get_image_path
def test_get_image_path(mock_file_manager):
    path = ImageFileHandler.get_image_path("image.jpg")
    assert path == "/base_path/image.jpg"


# Test save_image
def test_save_image(mock_image_save):
    mock_image = Image.new('RGB', (60, 30), color='red')
    ImageFileHandler.save_image(mock_image, "image.jpg")
    Image.Image.save.assert_called_once()


# Test get_image
def test_get_image(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="data"))
    result = ImageFileHandler.get_image("image.jpg")
    assert result == "data"


# Mock exists to always return True
def mock_exists(*args, **kwargs):
    return True


# Test delete_image
def test_delete_image(mocker):
    mocker.patch('pathlib.Path.exists', mock_exists)
    mock_unlink = mocker.patch('pathlib.Path.unlink')
    ImageFileHandler.delete_image("image.jpg")
    mock_unlink.assert_called_once()


def test_delete_image_without_path(mocker):
    result = ImageFileHandler.delete_image("incorrectname.jpg")
    assert result is None
