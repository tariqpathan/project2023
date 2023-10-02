# import pytest
# from unittest.mock import Mock
# from extraction_engine.managers.exam_manager import ExamManager
# from database.database_manager import DatabaseManager
# from database.models import Question
#
#
# @pytest.fixture
# def mock_db_manager():
#     return Mock(spec=DatabaseManager)
#
# @pytest.fixture
# def exam_manager(mock_db_manager):
#     return ExamManager(
#         exam_format='example_format',
#         question_pdf_path='question.pdf',
#         answer_pdf_path='answer.pdf',
#         db_manager=mock_db_manager
#     )
#
# def test_extract_data_from_pdfs(exam_manager, mocker):
#     mock_result = {'cover_details': {}, 'questions': [], 'answers': ''}
#     mocker.patch.object(exam_manager.pdf_manager, 'extract_pdf_data', return_value=mock_result)
#     result = exam_manager._extract_data_from_pdfs()
#     assert result == mock_result
#
# def test_process_questions(exam_manager, mocker):
#     mock_exam = Mock()
#     mock_questions_images = []
#     mock_result = [Mock(spec=Question)]
#     mocker.patch.object(exam_manager.question_manager, 'execute', return_value=mock_result)
#     result = exam_manager._process_questions(None, mock_exam, mock_questions_images)
#     assert result == mock_result
#
# def test_process_answers(exam_manager, mocker):
#     mock_text = 'example text'
#     mock_questions = [Mock(spec=Question)]
#     mocker.patch.object(exam_manager.answer_manager, 'execute')
#     exam_manager._process_answers(None, mock_text, mock_questions)
#     exam_manager.answer_manager.execute.assert_called_once_with(None, mock_text, mock_questions)
#
# def test_process(exam_manager, mocker):
#     mocker.patch.object(exam_manager, '_extract_data_from_pdfs', return_value={'cover_details': {}, 'questions': [], 'answers': ''})
#     mocker.patch.object(exam_manager.exam_factory, 'get_or_create_exam', return_value=Mock())
#     mocker.patch.object(exam_manager, '_process_questions', return_value=[Mock(spec=Question)])
#     mocker.patch.object(exam_manager, '_process_answers')
#
#     result = exam_manager.process()
#
#     assert result == 0
#     exam_manager._extract_data_from_pdfs.assert_called_once()
#     exam_manager._process_questions.assert_called_once()
#     exam_manager._process_answers.assert_called_once()
