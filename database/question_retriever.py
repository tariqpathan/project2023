import string
import random
import logging
from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import List

from database.models import Difficulty, Exam, HashQuestionMapping, Question, Subject, Subtopic
from database.database_utils import get_ids_from_names

logger = logging.getLogger(__name__)


class QuestionRetriever:

    FILTER_MAP = {
            'difficulty_levels': lambda x, session: Question.difficulty_id.in_(get_ids_from_names(session, Difficulty, x)),
            'subtopic_names': lambda x, session: Question.subtopics.any(Subtopic.id.in_(get_ids_from_names(session, Subtopic, x))),
            'subject_names': lambda x, session: Question.exam.has(Exam.subject_id.in_(get_ids_from_names(session, Subject, x))),
        }

    @classmethod
    def get_random_questions(cls, session: Session, num_questions: int, **filters) -> List[Question]:
        """
        Get a list of random questions based on provided filters.
        
        :param session: SQLAlchemy session object
        :param num_questions: Number of questions to retrieve
        :param filters: Additional filters for questions. Expected keys are:
            - difficulty_levels: List of difficulty levels
            - subtopic_names: List of subtopic names
            - subject_names: List of subject names
        :return: List of Question objects
        """
        query = session.query(Question)
        query_conditions = []

        for filter_name, filter_value in filters.items():
            if filter_name in cls.FILTER_MAP:
                query_conditions.append(cls.FILTER_MAP[filter_name](filter_value, session))

        if query_conditions:
            query = query.filter(and_(*query_conditions))

        all_ids = [x.id for x in query.all()]
        if not all_ids:
            return []

        random_ids = random.sample(all_ids, min(num_questions, len(all_ids)))
        return session.query(Question).filter(Question.id.in_(random_ids)).all()
    
    @staticmethod
    def check_code_unique(session: Session, code: str) -> bool:
        """Returns True if the hash is unique, False otherwise"""
        return session.query(HashQuestionMapping).filter(
            HashQuestionMapping.hash_str == code).count() == 0

    @staticmethod
    def generate_code(length:int = 6) -> str:
        letters = string.ascii_lowercase
        digits = string.digits
        random_letters = ''.join(random.choice(letters) for i in range(length - 2))
        random_digits = ''.join(random.choice(digits) for i in range(2))
        return random_letters + random_digits

    @staticmethod
    def get_questions_from_code(session: Session, hash_str: str) -> List[Question]:
        return session.query(Question).join(HashQuestionMapping).filter(
            HashQuestionMapping.hash_str == hash_str).all()
    
    @staticmethod
    def link_questions_with_code(session: Session, questions: List[Question]) -> str:
        unique = False
        hash_str = ''
        while not unique:
            hash_str = QuestionRetriever.generate_code()
            unique = QuestionRetriever.check_code_unique(session, hash_str)

        for q in questions:
            hash_question_mapping = HashQuestionMapping(hash_str=hash_str, question_id=q.id)
            session.add(hash_question_mapping)
        return hash_str
    

if __name__=="__main__":
    qr = QuestionRetriever()
    engine = None
    session = Session(bind=engine)
    kwargs = {}
    questions = qr.get_random_questions(session, 10)
    for q in questions:
        print(q.answer.answer_text)