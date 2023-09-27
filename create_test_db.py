import glob
import os

from database.database_manager import DatabaseManager
from database.models import Base, Subject, Exam

DATABASE_PATH = 'database/dbOne.db'


def initialize_database(db_manager):
    Base.metadata.drop_all(db_manager.engine)
    Base.metadata.create_all(db_manager.engine)


def add_data(db_manager):
    with db_manager as session:
        populate_db(session)
        session.commit()


def populate_db(session):
    # Create subjects
    biology = Subject(name='biology')
    chemistry = Subject(name='chemistry')
    physics = Subject(name='physics')

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


def load_db():
    db_manager = DatabaseManager(DATABASE_PATH)
    initialize_database(db_manager)
    add_data(db_manager)
    return db_manager


def delete_db(db_manager):
    Base.metadata.drop_all(db_manager.engine)


def delete_images():
    files = glob.glob('./static/question_images/*')
    for f in files:
        os.remove(f)
