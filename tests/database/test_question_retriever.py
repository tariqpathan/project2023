import pytest
from sqlalchemy.orm import Session

from database.models import Question, Difficulty, Subtopic, Exam, Subject
from database.question_retriever import QuestionRetriever

@pytest.fixture(scope="function")
def db_session():
    session = Session()
    yield session  # this is where the test function will execute
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def sample_data(db_session):
    # Populate the database with some sample data
    # Replace the following code with your actual models and fields
    difficulty = Difficulty(name='Easy')
    subtopic = Subtopic(name='plants')
    subject = Subject(name='biology')
    exam = Exam(name='Sample Exam', subject=subject)
    
    questions = [
        Question(text='What is 2+2?', difficulty=difficulty, subtopics=[subtopic], exam=exam),
        Question(text='What is 3+2?', difficulty=difficulty, subtopics=[subtopic], exam=exam)
    ]
    
    db_session.add_all(questions)
    db_session.commit()

def test_get_random_questions(db_session, sample_data):
    questions = QuestionRetriever.get_random_questions(db_session, 1)
    assert len(questions) == 1

def test_check_code_unique(db_session, sample_data):
    code = 'abcdef'
    is_unique = QuestionRetriever.check_code_unique(db_session, code)
    assert is_unique == True  # Assuming 'abcdef' is not in your test database

def test_generate_code():
    code = QuestionRetriever.generate_code(6)
    assert len(code) == 6  # Check if the length is correct

def test_get_questions_from_code(db_session, sample_data):
    # Here you might want to actually insert a HashQuestionMapping and then test if the function retrieves it
    pass  # Replace with your test

def test_link_questions_with_code(db_session, sample_data):
    questions = db_session.query(Question).all()
    code = QuestionRetriever.link_questions_with_code(db_session, questions)
    assert len(code) == 6  # or whatever you set your code length to
