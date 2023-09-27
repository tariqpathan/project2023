# Test for answer_factory.py
import pytest

from extraction_engine.factories.answer_factory import AnswerFactory


class TestAnswerFactory:

    # Set up a fixture to create a mock db_session
    # @pytest.fixture(scope="session")
    def mock_db_session(self, mocker):
        return mocker.Mock()

    # Test if the Answer object is created correctly
    def test_create_answer(self, mock_db_session, mocker):
        # Arrange
        answer_factory = AnswerFactory(db_session=mock_db_session)
        mock_question = mocker.Mock()
        mock_question.id = 1

        answer = mocker.Mock()
        answer.question_id = 1  # make sure this is a simple integer
        answer.answer_text = "correct answer"  # make sure this is a simple string

        # If you want to mock the Answer class itself
        mocker.patch('database.models.Answer', return_value=answer)

        # Act
        result = answer_factory.create_answer(mock_question, "correct answer")

        # Assert
        assert result.question.id == 1  # Now this should work
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
