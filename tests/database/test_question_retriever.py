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
    difficulty = Difficulty(level='Easy')
    subject = Subject(name='biology')
    subtopic = Subtopic(name='plants', subject=subject)
    subtopic_2 = Subtopic(name='animals', subject=subject)
    exam_test = Exam(exam_board="tariq", month="march", year=2020, unit_code="12", component_code="01", subject=subject)
    
    mapped_questions = [
        Question(image_filename='test1.jpg', question_number=1, difficulty=difficulty, subtopics=[subtopic], exam=exam_test),
        Question(image_filename='test2.jpg', question_number=2, difficulty=difficulty, subtopics=[subtopic_2], exam=exam_test)]
    
    unmapped_questions = [
        Question(image_filename='test3.jpg', question_number=3, exam=exam_test),
        Question(image_filename='test4.jpg', question_number=4, exam=exam_test),
        Question(image_filename='test5.jpg', question_number=5, exam=exam_test)]

    code_maps =  [
        QuestionCodeMapping(code_str='123456', question=mapped_questions[0]),
        QuestionCodeMapping(code_str='123456', question=mapped_questions[1])]

    question_ids = db_session.query(Question.id).all()
    print(question_ids)

    db_session.add_all([difficulty, subject, subtopic, subtopic_2, exam_test])
    db_session.add_all(mapped_questions)
    db_session.add_all(unmapped_questions)
    db_session.add_all(code_maps)
    db_session.commit()

def test_get_random_questions(db_session, sample_data):
    questions = QuestionRetriever.get_random_questions(db_session, 1)
    assert len(questions) == 1

def test_check_code_unique(db_session, sample_data):
    code = 'abcdef'
    code_in_table = '123456'
    assert QuestionRetriever.check_code_unique(db_session, code) == True
    assert QuestionRetriever.check_code_unique(db_session, code_in_table) == False


def test_generate_code():
    code = QuestionRetriever.generate_code(6)
    assert len(code) == 6
    assert code.isalnum() == True

def test_get_questions_with_correct_code(db_session, sample_data):
    code_in_table = '123456'
    questions = QuestionRetriever.get_questions_from_code(db_session, code_in_table)
    assert len(questions) == 2

def test_get_questions_with_incorrect_code(db_session, sample_data):
    code_in_table = '123450'
    questions = QuestionRetriever.get_questions_from_code(db_session, code_in_table)
    assert len(questions) == 0

def test_link_questions_with_code(db_session, sample_data):
    questions = db_session.query(Question).all()
    code = QuestionRetriever.link_questions_with_code(db_session, questions[2:])
    retrieved_questions = QuestionRetriever.get_questions_from_code(db_session, code)
    assert len(retrieved_questions) == 3    