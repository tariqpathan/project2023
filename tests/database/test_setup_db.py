# Test for create_db.py
import pytest

from database.database_manager import DatabaseManager
from database.models import Base, Subject


@pytest.fixture(scope='function')
def db_manager(tmpdir):
    db_path = tmpdir.join("test.db")
    db_manager = DatabaseManager(db_path)
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
        session.commit()
