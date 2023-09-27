# Test for question_factory.py
import os
from unittest.mock import Mock

import pytest
from PIL import Image

from database.models import Exam
from extraction_engine.factories.question_factory import QuestionFactory
from extraction_engine.managers.image_file_handler import ImageFileHandler


# Fixtures to setup necessary objects for testing
@pytest.fixture
def db_session_mock():
    return Mock()


@pytest.fixture
def exam_mock():
    exam = Exam()
    exam.id = 1
    exam.unit_code = "0625"
    return exam


@pytest.fixture
def question_factory(db_session_mock, exam_mock):
    return QuestionFactory(db_session_mock, exam_mock)


@pytest.fixture
def image():
    return Image.new('RGB', (60, 30), color=(73, 109, 137))


# Tests for QuestionFactory
def test_create_question(question_factory, image):
    question = question_factory.create_question(image, 1)
    assert question is not None
    assert question.exam.id == 1
    assert question.question_number == 1


# Tests for ImageFileHandler
def test_save_and_get_image(image, tmp_path):
    filename = "test_image.png"
    save_path = tmp_path / filename
    ImageFileHandler.save_image(image, str(save_path))
    assert save_path.exists()

    retrieved_image_data = ImageFileHandler.get_image(str(save_path))
    assert retrieved_image_data is not None

    # Cleanup
    if save_path.exists():
        os.remove(str(save_path))
