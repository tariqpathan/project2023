from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Difficulty, Exam, Question, Subject, Subtopic

DATABASE_PATH = "sqlite:///database/test.db"
engine = create_engine(DATABASE_PATH, echo=True)
Session = sessionmaker(bind=engine)
ScopedSession = scoped_session(Session)

def create_subject(name):
    with ScopedSession() as session, session.begin():
        new_subject = Subject(name=name)
        session.add(new_subject)

def update_subject_name(subject_id, new_name):
    with ScopedSession() as session:
        subject = session.query(Subject).filter_by(id=subject_id).first()
        if subject:
            subject.name = new_name

def delete_subject(subject_id):
    with ScopedSession() as session, session.begin():
        subject = session.query(Subject).filter_by(id=subject_id).first()
        if subject:
            session.delete(subject)

def get_all_subjects():
    with ScopedSession() as session:
        subjects = session.query(Subject).all()
    return subjects

def create_exam(exam_board, month, year, unit_code, component_code, subject_id):
    with ScopedSession() as session:
        new_exam = Exam(exam_board=exam_board, month=month, year=year, 
                    unit_code=unit_code, component_code=component_code, 
                    subject_id=subject_id)
        session.add(new_exam)

def delete_exam(exam_id):
    with ScopedSession() as session:
        exam = session.query(Exam).filter_by(id=exam_id).first()
        if exam:
            session.delete(exam)

def create_difficulty(level):
    with ScopedSession() as session:
        new_difficulty = Difficulty(level=level)
        session.add(new_difficulty)

def delete_difficulty(difficulty_id):
    with ScopedSession() as session:
        difficulty = session.query(Difficulty).filter_by(id=difficulty_id).first()
        if difficulty:
            session.delete(difficulty)

def create_subtopic(name, subject_id):
    with ScopedSession() as session:
        new_subtopic = Subtopic(name=name, subject_id=subject_id)
        session.add(new_subtopic)

def delete_subtopic(subtopic_id):
    with ScopedSession() as session:
        subtopic = session.query(Subtopic).filter_by(id=subtopic_id).first()
        if subtopic:
            session.delete(subtopic)

def create_question(image_path, question_number, correct_answer, difficulty_id, exam_id):
    with ScopedSession() as session:
        new_question = Question(image_path=image_path, question_number=question_number, 
                            correct_answer=correct_answer, difficulty_id=difficulty_id, 
                            exam_id=exam_id)
        session.add(new_question)

def update_question_number(question_id, question_number):
    with ScopedSession() as session:
        question = session.query(Question).filter_by(id=question_id).first()
        question.question_number = question_number

def update_question_answer(question_id, correct_answer):
    with ScopedSession() as session:
        question = session.query(Question).filter_by(id=question_id).first()
        question.correct_answer = correct_answer

def update_question_difficulty(question_id, difficulty):
    with ScopedSession() as session:
        question = session.query(Question).filter_by(id=question_id).first()
        question.difficulty = difficulty

def delete_question(question_id):
    with ScopedSession() as session:
        question = session.query(Question).filter_by(id=question_id).first()
        if question:
            session.delete(question)