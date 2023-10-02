# Test for CambridgeScienceAnswerProcessor.py
import pytest
from unittest.mock import Mock, patch
from PIL import Image
from extraction_engine.processing.cambridge_science_image_processor import CambridgeScienceImageProcessor

@pytest.fixture
def mock_image():
    img = Mock(spec=Image.Image)
    img.height = 100
    img.width = 100
    return img

@pytest.fixture
def config():
    return {
        "binary_threshold": 128,
        "margin_end": 20,
        "footer_height": 10,
        "padding": 2,
        "min_question_spacing": 5
    }

def test_init(mock_image, config):
    processor = CambridgeScienceImageProcessor(config)
    assert processor._config == config



