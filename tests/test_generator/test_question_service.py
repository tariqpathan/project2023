from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session
from database.models import Difficulty, Exam, Code, Question, Subject, Subtopic, Answer
from test_generator.question_service import QuestionService


# Mock the SQLAlchemy session
@pytest.fixture
def mock_session(mocker):
    return mocker.MagicMock()

@pytest.fixture
def question_service():
    return QuestionService()


def mock_get_image_path(*args, **kwargs):
    mock_path = MagicMock()
    mock_path.as_posix.return_value = args[0]
    return mock_path


def test_get_filter_names(question_service):
    filter_names = question_service.get_filter_names()
    expected_filters = ['difficulty_levels', 'subtopic_names', 'subject_names']
    assert filter_names == expected_filters


def test__select_random_questions(question_service, mock_session):
    mocked_questions = [MagicMock(spec=Question, id=i + 1) for i in range(10)]

    def mock_query(*args, **kwargs):
        mock_query_obj = MagicMock()
        mock_query_obj.filter.return_value.filter.return_value.all.return_value = mocked_questions
        return mock_query_obj

    mock_session.query.side_effect = mock_query

    questions = question_service._select_random_questions(mock_session, 10)
    assert isinstance(questions, list)
    assert all(isinstance(question, Question) for question in questions)


def test__generate_code(question_service):
    code = question_service._generate_code()
    assert len(code) == 6


def test__get_options(mock_session):
    mock_session.query().all.return_value = [
        Difficulty(level='Easy'),
        Difficulty(level='Medium'),
        Difficulty(level='Hard'),
    ]
    expected = ['Easy', 'Medium', 'Hard']
    assert QuestionService._get_options(mock_session, 'difficulty_levels') == expected


def test_get_all_options(mock_session):
    mock_session.query().all.side_effect = [
        [
            Difficulty(level='Easy'),
            Difficulty(level='Medium'),
            Difficulty(level='Hard'),
        ],
        [
            Subtopic(name='Algebra'),
            Subtopic(name='Geometry'),
            Subtopic(name='Trigonometry'),
        ],
        [
            Subject(name='Mathematics'),
            Subject(name='Physics'),
            Subject(name='Chemistry'),
        ],
    ]
    expected = {
        'difficulty_levels': ['Easy', 'Medium', 'Hard'],
        'subtopic_names': ['Algebra', 'Geometry', 'Trigonometry'],
        'subject_names': ['Mathematics', 'Physics', 'Chemistry'],
    }
    assert QuestionService.get_all_options(mock_session) == expected


def test__check_code_unique(mock_session):
    mock_session.query().filter().count.return_value = 0
    assert QuestionService._check_code_unique(mock_session, 'unique_code')

    mock_session.query().filter().count.return_value = 1
    assert not QuestionService._check_code_unique(mock_session, 'non_unique_code')


def test__link_questions_with_code(mock_session):
    mock_session.query().filter().count.return_value = 0
    mock_session.query().filter().count.side_effect = [0, 1]
    mock_session.query().filter().first.return_value = None
    code = QuestionService._link_questions_with_code(mock_session, [Question()])
    assert isinstance(code, str)
    assert len(code) == 6


def test__link_questions_with_code_failure(mock_session):
    mock_session.query.return_value.filter.return_value.count.return_value = 1  # Always non-unique

    with pytest.raises(Exception, match="Failed to generate a unique code."):
        QuestionService._link_questions_with_code(mock_session, [Question()])

def test_get_questions_with_code(monkeypatch, mock_session):
    monkeypatch.setattr(
        "extraction_engine.managers.image_file_handler.ImageFileHandler.get_image_path",
        mock_get_image_path)

    code = Code(
        code_str='code123',
        questions=[
            Question(
                id=1,
                image_filename='question1.png',
                answer=Answer(answer_text='Answer 1')
            ),
            Question(
                id=2,
                image_filename='question2.png',
                answer=Answer(answer_text='Answer 2')
            ),
            Question(
                id=3,
                image_filename='question3.png',
                answer=Answer(answer_text='Answer 3')
            ),
        ]
    )

    # Configure the mock session to return the mock Code object
    mock_session.query().filter().options().one_or_none.return_value = code

    # Call the get_questions_with_code method with the mock session and check the results
    result = QuestionService.get_questions_with_code(mock_session, 'code123', answers=True)
    assert result == {
        'code': 'code123',
        'result': [
            {
                'id': 1,
                'question': 'question1.png',
                'answer': 'Answer 1'
            },
            {
                'id': 2,
                'question': 'question2.png',
                'answer': 'Answer 2'
            },
            {
                'id': 3,
                'question': 'question3.png',
                'answer': 'Answer 3'
            },
        ]
    }

    def test_get_questions_with_invalid_code(mock_session):
        # Configure the mock session to return None
        mock_session.query().filter().options().one_or_none.return_value = None

        # Call the get_questions_with_code method with the mock session and check the results
        result = QuestionService.get_questions_with_code(mock_session, 'code123', answers=True)
        assert result == {
            'code': None,
            'result': []
        }
