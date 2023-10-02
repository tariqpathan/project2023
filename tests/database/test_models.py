import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database.models import Base, Code, Subject, Exam, Difficulty, Question, Answer, Subtopic


@pytest.fixture(scope='function')
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope='function')
def basic_data():
    subject = Subject(name='English')
    exam = Exam(exam_board='AQA', month='June', year=2022, unit_code='U1', component_code='C1', subject=subject)
    difficulty = Difficulty(level='Easy')
    question = Question(image_filename='test.jpg', question_number=1, exam=exam, difficulty=difficulty)
    answer = Answer(question=question, answer_text='Answer')
    subtopic = Subtopic(name='Poetry', subject=subject)
    code = Code(code_str='123456')

    return {"subject": subject, "exam": exam, "difficulty": difficulty,
            "question": question, "answer": answer, "subtopic": subtopic, "code": code}


def test_insertions(db_session, basic_data):
    db_session.add_all(basic_data.values())
    db_session.commit()

    for key, value in basic_data.items():
        fetched_value = db_session.query(type(value)).first()
        assert fetched_value is not None  # Make sure object exists

        # Loop through each attribute in the original object
        for attr in vars(value):
            if attr.startswith('_'):
                continue  # Skip internal attributes
            original_value = getattr(value, attr)
            fetched_attr_value = getattr(fetched_value, attr)
            assert original_value == fetched_attr_value

        # Check the count for each model type
        assert db_session.query(type(value)).count() == 1


# Test relationship between Subject and Exam
def test_exam_subject_relation(db_session):
    subject = Subject(name='Math')
    exam = Exam(exam_board='Board', month='Jan', year=2022, unit_code='101', component_code='01', subject=subject)

    db_session.add(subject)
    db_session.add(exam)
    db_session.commit()

    fetched_exam = db_session.query(Exam).first()
    assert fetched_exam.subject.name == 'Math'


# Test relationship between Question and Exam
def test_question_exam_relation(db_session):
    subject = Subject(name='Math')
    exam = Exam(exam_board='Board', month='Jan', year=2022, unit_code='101', component_code='01', subject=subject)
    question = Question(image_filename='test.jpg', question_number=1, exam=exam)

    db_session.add(subject)
    db_session.add(exam)
    db_session.add(question)
    db_session.commit()

    fetched_question = db_session.query(Question).first()
    assert fetched_question.exam.exam_board == 'Board'


# Test relationship between Question and Difficulty
def test_question_difficulty_relation(db_session):
    exam = Exam(exam_board='Board', month='Jan', year=2022, unit_code='101', component_code='01')
    db_session.add(exam)
    difficulty = Difficulty(level='Easy')
    question = Question(image_filename='test.jpg', question_number=1, difficulty=difficulty, exam=exam)

    db_session.add(difficulty)
    db_session.add(question)
    db_session.commit()

    fetched_question = db_session.query(Question).first()
    assert fetched_question.difficulty.level == 'Easy'


# Test unique constraint for Subject.name
def test_unique_subject_name(db_session):
    subject1 = Subject(name='Math')
    subject2 = Subject(name='Math')

    db_session.add(subject1)
    db_session.commit()

    db_session.add(subject2)
    with pytest.raises(IntegrityError):
        db_session.commit()


# Assuming Exam has a unique constraint on unit_code and component_code
def test_unique_exam_code(db_session):
    subject = Subject(name='Math')
    db_session.add(subject)
    exam1 = Exam(exam_board='Board', month='Jan', year=2022, unit_code='101', component_code='01', subject=subject)
    exam2 = Exam(exam_board='Board', month='Jan', year=2022, unit_code='101', component_code='01', subject=subject)


    db_session.add(exam1)
    db_session.commit()

    db_session.add(exam2)
    with pytest.raises(IntegrityError):
        db_session.commit()
