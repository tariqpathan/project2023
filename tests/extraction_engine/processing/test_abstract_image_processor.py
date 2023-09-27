# Test for AbstractImageProcessor.py
from unittest.mock import Mock

from extraction_engine.processing.abstract_image_processor import AbstractImageProcessor


def test_convert_to_grayscale_image():
    mock_img = Mock()
    result = AbstractImageProcessor._convert_to_grayscale_image(mock_img)
    mock_img.convert.assert_called_once_with('L')
    assert result == mock_img.convert.return_value


def test_convert_to_binary_image():
    mock_img = Mock()
    threshold = 128
    result = AbstractImageProcessor._convert_to_binary_image(mock_img, threshold)
    mock_img.point.assert_called_once()
    assert result == mock_img.point.return_value
