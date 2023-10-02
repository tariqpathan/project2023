# Test for answer_factory.py
import pytest
from database.models import Answer, Question
from extraction_engine.factories.answer_factory import AnswerFactory


@pytest.fixture(scope="function")
def mock_db_session(mocker):
    return mocker.Mock()


class TestAnswerFactory:
    def test_create_answer(self, mock_db_session, mocker):
        # Arrange
        answer_factory = AnswerFactory(db_session=mock_db_session)

        mock_question = mocker.Mock()
        mock_question.id = 1

        mock_answer = mocker.Mock()
        mock_answer.question_id = 1
        mock_answer.answer_text = "correct answer"

        mocker.patch('database.models.Answer', return_value=mock_answer)

        # Act
        result = answer_factory.create_answer(mock_question, "correct answer")

        # Assert
        assert result.question_id == 1
        assert result.answer_text == "correct answer"
        mock_db_session.add.assert_called_with(result)

    # Test if an exception is thrown when db_session.add fails
    def test_create_answer_exception(self, mock_db_session, mocker):
        # Arrange
        answer_factory = AnswerFactory(db_session=mock_db_session)
        mock_db_session.add.side_effect = Exception("DB Error")
        mock_question = mocker.Mock()
        mock_question.id = 1

        # Act and Assert
        with pytest.raises(Exception) as excinfo:
            answer_factory.create_answer(mock_question, "correct answer")

        assert "Error creating Answer" in str(excinfo.value)
