# Test for database_utils.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Question, Difficulty, Subtopic, Exam, Subject, QuestionCodeMapping
from database.question_retriever import QuestionRetriever

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # this is where the test function will execute
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def sample_data(db_session):
    # Populate the database with some sample data
    # Replace the following code with your actual models and fields
    difficulty = Difficulty(level='Easy')
    subject = Subject(name='biology')
    subtopic = Subtopic(name='plants', subject=subject)
    subtopic_2 = Subtopic(name='animals', subject=subject)
    exam_test = Exam(exam_board="tariq", month="march", year=2020, unit_code="12", component_code="01", subject=subject)
    
    questions = [
        Question(image_filename='test1.jpg', question_number=1, difficulty=difficulty, subtopics=[subtopic], exam=exam_test),
        Question(image_filename='test2.jpg', question_number=2, difficulty=difficulty, subtopics=[subtopic_2], exam=exam_test),
    ]
    db_session.add_all([difficulty, subject, subtopic, subtopic_2, exam_test])
    db_session.add_all(questions)
    db_session.commit()

def test_get_random_questions(db_session, sample_data):
    questions = QuestionRetriever.get_random_questions(db_session, 1)
    assert len(questions) == 1