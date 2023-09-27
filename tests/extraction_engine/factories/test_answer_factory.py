# Test for answer_factory.py
import pytest
from database.models import Answer, Question
from extraction_engine.factories.answer_factory import AnswerFactory  

class TestAnswerFactory:
    
    # Set up a fixture to create a mock db_session
    @pytest.fixture
    def mock_db_session(self, mocker):
        return mocker.MagicMock()
    
    # Test if the Answer object is created correctly
    def test_create_answer(self, mock_db_session):
        # Arrange
        answer_factory = AnswerFactory(db_session=mock_db_session)
        mock_question = Question()
        mock_question.id = 1
        
        # Act
        answer = answer_factory.create_answer(mock_question, "correct answer")
        
        # Assert
        assert answer.question_id == mock_question.id
        assert answer.answer_text == "correct answer"
        mock_db_session.add.assert_called_once_with(answer)
    
    # Test if an exception is thrown when db_session.add fails
    def test_create_answer_exception(self, mock_db_session):
        # Arrange
        answer_factory = AnswerFactory(db_session=mock_db_session)
        mock_db_session.add.side_effect = Exception("DB Error")
        mock_question = Question()
        mock_question.id = 1
        
        # Act and Assert
        with pytest.raises(Exception) as excinfo:
            answer_factory.create_answer(mock_question, "correct answer")
        
        assert "Error creating Answer" in str(excinfo.value)




# class TestAnswerFactory2:

#     # Test if the Answer object is created correctly
#     def test_create_answer(self, monkeypatch):
#         mock_db_session = pytest.Mock()

#         # Patch the 'add' method of db_session
#         monkeypatch.setattr(mock_db_session, 'add', pytest.Mock())

#         # Arrange
#         answer_factory = AnswerFactory(db_session=mock_db_session)
#         mock_question = Question()
#         mock_question.id = 1

#         # Act
#         answer = answer_factory.create_answer(mock_question, "correct answer")

#         # Assert
#         assert answer.question_id == mock_question.id
#         assert answer.answer_text == "correct answer"
#         mock_db_session.add.assert_called_once_with(answer)

#     # Test if an exception is thrown when db_session.add fails
#     def test_create_answer_exception(self, monkeypatch):
#         mock_db_session = pytest.Mock()

#         # Patch the 'add' method of db_session to raise an Exception
#         monkeypatch.setattr(mock_db_session, 'add', pytest.Mock(side_effect=Exception("DB Error")))

#         # Arrange
#         answer_factory = AnswerFactory(db_session=mock_db_session)
#         mock_question = Question()
#         mock_question.id = 1

#         # Act and Assert
#         with pytest.raises(Exception) as excinfo:
#             answer_factory.create_answer(mock_question, "correct answer")

#         assert "Error creating Answer" in str(excinfo.value)
