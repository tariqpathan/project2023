import logging
import yaml
from pathlib import Path
from database.models import Base, Subject, Subtopic
from typing import Type, TypeVar, Optional
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

FILEPATH = Path(__file__).parents[1] / 'config' / 'subjects.yaml'

def get_subjects_from_config():
    with open(FILEPATH, 'r') as file:
        data = yaml.safe_load(file)
    return data['topics']

ModelType = TypeVar("ModelType", bound=Base)
def insert_or_ignore_model(session, model_class: Type[ModelType], **kwargs) -> Optional[ModelType]:
    new_instance = model_class(**kwargs)
    session.add(new_instance)
    try:
        session.flush()  # Attempt to add the new record
        return new_instance  # Return the ID of the new instance
    except IntegrityError:  # Handle duplicates
        session.rollback()  # Rollback if duplicate exists
        existing_instance = session.query(model_class).filter_by(**kwargs).first()
        return existing_instance

def count_subjects(session, data) -> bool:
    # db_num_subtopics = session.query(Subtopic).count()
    # num_subtopics = sum(len(topic) for topic in data.values())
    db_num_subjects = session.query(Subject).count()
    num_subjects = len(data)
    return db_num_subjects == 0 or db_num_subjects < num_subjects

def update_subjects(session, data):
    for s, topic_list in data.items():
        subject = insert_or_ignore_model(session, Subject, name=s)
        if subject is None: continue
        for topic_name in topic_list:
            insert_or_ignore_model(session, Subtopic, name=topic_name, subject_id=subject.id)
    session.commit()

def initial_setup(db_manager):
    logging.info("Creating database tables")
    data = get_subjects_from_config()
    with db_manager.get_session() as session:
        if count_subjects(session, data):
            update_subjects(session, data)
    logging.info("Database updated")


