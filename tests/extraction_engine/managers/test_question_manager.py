# Test for question_manager.py
import pytest
from unittest.mock import Mock, patch
from extraction_engine.managers.question_manager import QuestionManager
from PIL import Image
from database.models import Exam
from extraction_engine.processing.abstract_image_processor import AbstractImageProcessor
from extraction_engine.processing.image_text_processor import ImageTextProcessor


@pytest.fixture
def mock_image_processor():
    return Mock(spec=AbstractImageProcessor)


@pytest.fixture
def mock_text_processor():
    return Mock(spec=ImageTextProcessor)


@pytest.fixture
def mock_config_manager():
    mock = Mock()
    mock.get_config.return_value = {
        "imageProcessor": {},
        "textProcessor": {}
    }
    return mock


@pytest.fixture
def question_manager(mock_config_manager, mock_image_processor, mock_text_processor):
    with patch.object(QuestionManager, "_get_image_processor", return_value=mock_image_processor), \
            patch.object(QuestionManager, "_get_text_processor", return_value=mock_text_processor):
        return QuestionManager(exam_format="some_format")


def test_validate_processor(question_manager, mock_image_processor):
    image = Image.new('RGB', (60, 30))
    question_manager.validate_processor(image)
    mock_image_processor.validate.assert_called_once_with(image)


def test_extract_questions(question_manager, mock_image_processor):
    image = Image.new('RGB', (60, 30))
    mock_image_processor.extract.return_value = [Image.new('RGB', (60, 30))]
    result = question_manager._extract_questions(image)
    mock_image_processor.extract.assert_called_once_with(image)
    assert len(result) == 1


def test_get_question_number(question_manager, mock_text_processor):
    image = Image.new('RGB', (60, 30))
    mock_text_processor.get_question_number.return_value = 1
    result = question_manager._get_question_number(image)
    mock_text_processor.get_question_number.assert_called_once_with(image)
    assert result == 1




def test_create_question(question_manager):
    image = Image.new('RGB', (60, 30))
    qnum = 1
    with patch('extraction_engine.factories.question_factory.QuestionFactory') as mock_question_factory:
        mock_question_factory.create_question.return_value = Mock()
        question_manager.question_factory = mock_question_factory
        question = question_manager._create_question(image, qnum)
    mock_question_factory.create_question.assert_called_once_with(image, qnum)
    assert question is not None


def test_process_images(question_manager):
    images = [Image.new('RGB', (60, 30))]
    with patch.object(question_manager, '_extract_questions', return_value=images) as mock_extract_questions, \
            patch.object(question_manager, '_get_question_number', return_value=1) as mock_get_question_number, \
            patch.object(question_manager, '_post_process', return_value=images[0]) as mock_post_process:
        question_nums, post_processed_images = question_manager._process_images(images)

    mock_extract_questions.assert_called_once()
    mock_get_question_number.assert_called_once()
    mock_post_process.assert_called_once()
    assert question_nums == [1]
    assert post_processed_images == images


def test_execute(question_manager):
    db_session = Mock()
    exam = Mock(spec=Exam)
    images = [Image.new('RGB', (60, 30))]

    # mock the methods that will be called within execute
    with patch.object(question_manager, "_set_question_factory") as mock_set_question_factory, \
            patch.object(question_manager, "validate_processor") as mock_validate_processor, \
            patch.object(question_manager, "_process_images") as mock_process_images, \
            patch.object(question_manager, "_create_question") as mock_create_question:
        mock_process_images.return_value = ([1], [Image.new('RGB', (60, 30))])
        mock_create_question.return_value = Mock()  # mock a Question object

        result = question_manager.execute(db_session, exam, images)

    mock_set_question_factory.assert_called_once_with(db_session, exam)
    mock_validate_processor.assert_called_once_with(images[0])
    mock_process_images.assert_called_once_with(images)
    mock_create_question.assert_called_once_with(images[0], 1)
    assert len(result) == 1  # since we mocked a single question to be returned
