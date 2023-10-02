
from database.models import Exam, Subject, Subtopic, Difficulty


def get_subject_id(session, subject_name):
    """Retrieve the ID of the subject with the given name."""
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    if subject:
        return subject.id
    else:
        raise ValueError(f"Subject with name {subject_name} does not exist.")

def get_all_subjects(session):
    return [s.name for s in session.query(Subject.name).all()]

def get_ids_from_names(session, model, names):
    return [item.id for item in session.query(model.id).filter(model.name.in_(names)).all()]


# def get_from_name(session, model, name):
#     return session.query(model).filter(model.name == name).first()

def get_all_difficulties(session):
    return [d.level for d in session.query(Difficulty.level).all()]

def get_subtopic_for_subject(session, subject_id=None):
    query = session.query(Subtopic.name)
    if subject_id:
        query = query.filter(Subtopic.subject_id == subject_id)
    return [s.name for s in query.all()]

def get_all_subtopics(session):
    return [s.name for s in session.query(Subtopic.name).distinct(Subtopic.name).all()]