# Test for answer_manager.py
import pytest
from unittest.mock import Mock, patch, create_autospec, MagicMock
from extraction_engine.managers.answer_manager import AnswerManager
from database.models import Answer, Question

@pytest.fixture
def mock_db_session():
    return Mock()

@pytest.fixture
def mock_question():
    return create_autospec(Question, instance=True)

@pytest.fixture
def answer_manager():
    return AnswerManager(exam_format='cambridge_science')

def test_initialization(answer_manager):
    assert isinstance(answer_manager, AnswerManager)
    assert answer_manager.exam_format == 'cambridge_science'

def test_get_answer_processor(answer_manager):
    with patch('extraction_engine.managers.answer_manager.AnswerProcessorFactory.create_processor', return_value=Mock()) as mock_method:
        processor = answer_manager._get_answer_processor()
    mock_method.assert_called_once_with('cambridge_science')
    assert processor is not None

def test_set_answer_factory(answer_manager, mock_db_session):
    answer_manager._set_answer_factory(mock_db_session)
    assert answer_manager.answer_factory is not None

def test_execute(answer_manager, mock_db_session, mock_question):
    text = 'some text'
    questions = [mock_question]

    # Mock the process method to return a non-empty dictionary
    answer_manager.answer_processor.process = MagicMock(return_value={'some_key': 'some_value'})

    with patch.object(answer_manager, '_match_questions') as mock_method:
        answer_manager.execute(mock_db_session, text, questions)
    mock_method.assert_called_once()


def test_match_questions(answer_manager, mock_question):
    mock_answer_factory = Mock()
    answer_manager.answer_factory = mock_answer_factory  # Manually assign the mock object

    qnum_answer_dict = {1: 'Answer text'}
    mock_question.question_number = 1
    questions = [mock_question]

    answer_manager._match_questions(qnum_answer_dict, questions)

    mock_answer_factory.create_answer.assert_called_once_with(mock_question, 'Answer text')


