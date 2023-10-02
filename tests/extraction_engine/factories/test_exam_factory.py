# Test for exam_factory.py
import pytest
from unittest.mock import Mock, MagicMock
from extraction_engine.factories.exam_factory import ExamFactory
from database.models import Exam, Subject

@pytest.fixture
def mock_session():
    return Mock()

@pytest.fixture
def mock_subject():
    subject = Subject(name='English')
    subject.id = 1
    return subject

@pytest.fixture
def mock_exam():
    exam = Exam()
    exam.subject_id = 1
    return exam

@pytest.fixture
def exam_factory():
    return ExamFactory()

def test_normalise_exam_data(exam_factory, mock_session, mock_subject):
    mock_session.query().filter().first.return_value = mock_subject
    input_data = {'subject': 'Math'}
    output_data = exam_factory._normalise_exam_data(mock_session, input_data)
    assert 'subject_id' in output_data
    assert output_data['subject_id'] == 1

def test_get_or_create_exam_when_exam_exists(exam_factory, mock_session, mock_exam):
    mock_session.query().filter().first.return_value = mock_exam
    input_data = {
        'subject_id': 1,
        'exam_board': 'XYZ',
        'month': 'June',
        'year': 2022,
        'unit_code': '1234',
        'component_code': '5678'
    }
    result = exam_factory.get_or_create_exam(mock_session, input_data)
    assert result is mock_exam

def test_get_or_create_exam_when_exam_not_exists(exam_factory, mock_session, mock_subject):
    mock_subject.id = 1
    mock_session.query().filter().first.side_effect = [None, mock_exam]
    input_data = {
        'subject_id': 1,
        'exam_board': 'XYZ',
        'month': 'June',
        'year': 2022,
        'unit_code': '1234',
        'component_code': '5678'
    }
    result = exam_factory.get_or_create_exam(mock_session, input_data)
    assert result is not None
    assert result.subject_id == 1
    mock_session.add.assert_called_with(result)
