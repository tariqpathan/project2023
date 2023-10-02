# Test for database_utils.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Code, Question, Difficulty, Subtopic, Exam, Subject
import database.database_utils as dbu

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
    exam = Exam(exam_board="tariq", month="march", year=2020, unit_code="12", component_code="01", subject=subject)
    code = Code(code_str='123456')
    
    questions = [
        Question(image_filename='test1.jpg', question_number=1, difficulty=difficulty, subtopics=[subtopic], exam=exam),
        Question(image_filename='test2.jpg', question_number=2, difficulty=difficulty, subtopics=[subtopic_2], exam=exam),
    ]
    db_session.add_all([difficulty, subject, subtopic, subtopic_2, exam])
    db_session.add_all(questions)
    db_session.commit()


def test_get_subject_id(db_session):
    sub1 = Subject(name='Math')
    db_session.add(sub1)
    db_session.commit()

    assert dbu.get_subject_id(db_session, 'Math') == sub1.id
    with pytest.raises(ValueError):
        dbu.get_subject_id(db_session, 'Physics')

def test_list_subject_names(db_session):
    sub1 = Subject(name='Math')
    sub2 = Subject(name='Physics')
    db_session.add_all([sub1, sub2])
    db_session.commit()

    assert dbu.get_all_subjects(db_session) == ['Math', 'Physics']

def test_get_ids_from_names(db_session):
    sub1 = Subject(name='Math')
    sub2 = Subject(name='Physics')
    db_session.add_all([sub1, sub2])
    db_session.commit()

    assert dbu.get_ids_from_names(db_session, Subject, ['Math', 'Physics']) == [sub1.id, sub2.id]

# def test_get_from_name(db_session):
#     sub1 = Subject(name='Math')
#     db_session.add(sub1)
#     db_session.commit()

#     assert dbu.get_from_name(db_session, Subject, 'Math') == sub1

def test_list_available_difficulties(db_session):
    diff1 = Difficulty(level='Easy')
    diff2 = Difficulty(level='Hard')
    db_session.add_all([diff1, diff2])
    db_session.commit()

    assert dbu.get_all_difficulties(db_session) == ['Easy', 'Hard']

def test_list_available_subtopics(db_session):
    sub1 = Subject(name='Math')
    subtopic1 = Subtopic(name='Algebra', subject=sub1)
    db_session.add_all([sub1, subtopic1])
    db_session.commit()

    assert dbu.get_subtopic_for_subject(db_session) == ['Algebra']
    assert dbu.get_subtopic_for_subject(db_session, subject_id=sub1.id) == ['Algebra']

def test_list_all_subtopics(db_session):
    sub1 = Subject(name='Math')
    subtopic1 = Subtopic(name='Algebra', subject=sub1)
    sub2 = Subject(name='Physics')
    subtopic2 = Subtopic(name='Mechanics', subject=sub2)
    db_session.add_all([sub1, subtopic1, sub2, subtopic2])
    db_session.commit()

    assert dbu.get_all_subtopics(db_session) == ['Algebra', 'Mechanics']
