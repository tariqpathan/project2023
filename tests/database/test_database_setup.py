# Test for create_db.py
from database.models import Base, Subject, Exam
from database.database_manager import DatabaseManager
from sqlalchemy.exc import IntegrityError
import pytest

@pytest.fixture(scope='function')
def db_manager():
    db_manager = DatabaseManager(":memory:")
    Base.metadata.create_all(db_manager.engine)
    yield db_manager  # this is where the testing happens
    Base.metadata.drop_all(db_manager.engine)

def test_add_subject(db_manager):
    with db_manager as session:
        subject = Subject(name='Math')
        session.add(subject)
        session.commit()

        assert session.query(Subject).count() == 1
        assert session.query(Subject).first().name == 'Math'

        subject = Subject(name='Math')
        session.add(subject)
        with pytest.raises(IntegrityError):
            session.commit()