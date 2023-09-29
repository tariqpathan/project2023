from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path
from typing import Union

from database.models import Base

class DatabaseManager:
    def __init__(self, db_path: Union[str, Path], echo: bool = False):
        path = Path(db_path).as_posix() if isinstance(db_path, Path) else db_path
        self.engine = create_engine(f'sqlite:///{path}', echo=echo)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)
        self.session = None
    
    def get_session(self):
        if not self.session:
            self.session = self.Session()
        return self.session

    def __enter__(self):
        return self.get_session()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            self.session.close()
    
    def commit(self):
        if self.session:
            self.session.commit()

    def rollback(self):
        if self.session:
            self.session.rollback()
    