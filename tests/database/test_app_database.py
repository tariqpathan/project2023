import os

from database.database_manager import DatabaseManager
from database.models import Base, Subject, Exam

DATABASE_PATH = 'tests/database/test.db'


def initialize_database():
    Base.metadata.create_all(db_manager.engine)


def add_data(db_manager):
    with db_manager as session:
        populate_db(session)
        query_data(session)
        session.commit()


def destroy_database():
    Base.metadata.drop_all(db_manager.engine)
    os.remove(DATABASE_PATH)


def populate_db(session):
    # Create subjects
    biology = Subject(name='Biology')
    chemistry = Subject(name='Chemistry')
    physics = Subject(name='Physics')

    # Create exams
    exams = [
        Exam(exam_board='Edexcel', month='June', year=2022, unit_code='U1', component_code='C1', subject=biology),
        Exam(exam_board='AQA', month='June', year=2022, unit_code='U2', component_code='C2', subject=chemistry),
        Exam(exam_board='OCR', month='January', year=2022, unit_code='U3', component_code='C3', subject=physics),
        Exam(exam_board='Edexcel', month='June', year=2021, unit_code='U4', component_code='C4', subject=biology),
        Exam(exam_board='AQA', month='June', year=2021, unit_code='U5', component_code='C5', subject=chemistry)
    ]

    # Add subjects and exams to session
    session.add_all([biology, chemistry, physics] + exams)
    print("Added data to database")


def query_data(session):
    exam_data = {'exam_board': 'OCR'}
    exam = session.query(Exam).filter_by(**exam_data).first()
    print(exam.subject.name)


if __name__ == '__main__':
    db_manager = DatabaseManager(DATABASE_PATH)
    initialize_database()
    add_data(db_manager)
    destroy_database()
