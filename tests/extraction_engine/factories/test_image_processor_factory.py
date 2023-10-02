import pytest
from extraction_engine.factories.image_processor_factory import ImageProcessorFactory
from extraction_engine.processing.abstract_image_processor import AbstractImageProcessor
from extraction_engine.processing.cambridge_science_image_processor import CambridgeScienceImageProcessor

def test_create_processor():
    config = {}  # Assume an empty config for simplicity
    processor = ImageProcessorFactory.create_processor("cambridge_science", config)
    assert isinstance(processor, CambridgeScienceImageProcessor)

def test_create_processor_invalid_exam_format():
    config = {}  # Assume an empty config for simplicity
    with pytest.raises(ValueError) as excinfo:
        ImageProcessorFactory.create_processor("invalid_format", config)
    assert str(excinfo.value) == "No processor found for exam board 'invalid_format'"

def test_create_processor_returns_abstract_image_processor():
    config = {}  # Assume an empty config for simplicity
    processor = ImageProcessorFactory.create_processor("cambridge_science", config)
    assert isinstance(processor, AbstractImageProcessor)
