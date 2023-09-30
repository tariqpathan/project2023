import string
import random
import logging
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from typing import Dict, List, Any

from database.models import Difficulty, Exam, Code, Question, Subject, Subtopic, Answer
from database.database_utils import get_ids_from_names

logger = logging.getLogger(__name__)


class QuestionService:
    FILTER_MAP = {
        'difficulty_levels': lambda x, session: Question.difficulty_id.in_(get_ids_from_names(session, Difficulty, x)),
        'subtopic_names': lambda x, session: Question.subtopics.any(
            Subtopic.id.in_(get_ids_from_names(session, Subtopic, x))),
        'subject_names': lambda x, session: Question.exam.has(
            Exam.subject_id.in_(get_ids_from_names(session, Subject, x))),
    }

    ATTRIBUTE_MAP = {
        'difficulty_levels': ('Difficulty', 'level'),
        'subtopic_names': ('Subtopic', 'name'),
        'subject_names': ('Subject', 'name'),
    }

    @classmethod
    def get_filter_names(cls) -> List[str]:
        """Returns a list of valid filter names."""
        return list(cls.FILTER_MAP.keys())

    @classmethod
    def _get_options(cls, session: Session, filter_name: str) -> List[str]:
        """Returns all possible options for a given filter name."""
        model_name, attribute_name = cls.ATTRIBUTE_MAP.get(filter_name, (None, None))
        if not model_name or not attribute_name:
            return []
        model_class = globals()[model_name]  # Use the globals() function to get the class by its name
        return [getattr(item, attribute_name) for item in session.query(model_class).all()]

    @classmethod
    def get_all_options(cls, session: Session) -> Dict[str, List[str]]:
        """Returns a dictionary of all valid filter names and their corresponding options."""
        return {filter_name: cls._get_options(session, filter_name) for filter_name in cls.get_filter_names()}

    @staticmethod
    def _check_code_unique(session: Session, code: str) -> bool:
        """Returns True if the hash is unique, False otherwise"""
        return session.query(Code).filter(
            Code.code_str == code).count() == 0

    @staticmethod
    def _generate_code(length: int = 6) -> str:
        letters = string.ascii_lowercase
        digits = string.digits
        random_letters = ''.join(random.choice(letters) for i in range(length - 2))
        random_digits = ''.join(random.choice(digits) for i in range(2))
        return random_letters + random_digits

    @classmethod
    def _link_questions_with_code(cls, session: Session, questions: List[Question]) -> str:
        unique = False
        code_str = ''
        while not unique:
            code_str = cls._generate_code()
            unique = cls._check_code_unique(session, code_str)
        code = Code(code_str=code_str)
        session.add(code)
        code.questions.extend(questions)
        return code.code_str

    @classmethod
    def _select_random_questions(cls, session: Session, num_questions: int, **filters) -> List[Question]:
        """
        Get a list of random questions based on provided filters.
        
        :param session: SQLAlchemy session object
        :param num_questions: Number of questions to retrieve
        :param answers: If True, only questions with answers will be returned
        :param filters: Additional filters for questions. Expected keys are:
            - difficulty_levels: List of difficulty levels
            - subtopic_names: List of subtopic names
            - subject_names: List of subject names
        :return: List of Question objects
        """

        # Question.id == Answer.question_id makes sure than an answer exists
        query = session.query(Question).filter(Question.id == Answer.question_id)
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

    @classmethod
    def generate_questions(cls, session: Session, num_questions: int, answers: bool = True, **filters) -> Dict[
        str, Any]:
        """
        Generate a list of random questions based on provided filters.

        :param session: SQLAlchemy session object
        :param num_questions: Number of questions to retrieve
        :param answers: If True, only questions with answers will be returned
        :param filters: Additional filters for questions. Expected keys are:
            - difficulty_levels: List of difficulty levels
            - subtopic_names: List of subtopic names
            - subject_names: List of subject names
        :return: Dictionary containing the code and a list of Question objects
        """
        selected_questions = cls._select_random_questions(session, num_questions, **filters)
        code = cls._link_questions_with_code(session, selected_questions)
        return cls.get_questions_with_code(session, code, answers)

    @staticmethod
    def get_questions_with_code(session: Session, code_str: str,
                                answers: bool = True, **filters) -> dict[Any, Any]:
        code = session.query(Code) \
            .filter(Code.code_str == code_str) \
            .options(joinedload(Code.questions).joinedload(Question.answer)) \
            .one_or_none()
        if not code:
            return []
        questions = code.questions

        return {
            'code': code.code_str,
            'result': [
                {
                    'id': q.id,
                    'question': q.image_filename,
                    'answer': q.answer.answer_text if answers else None
                }
                for q in questions
            ]
        }


if __name__ == "__main__":
    from database.database_manager import DatabaseManager
    from extraction_engine.managers.file_manager import FileManager

    db_path = FileManager.get_filepaths("db_path")
    db_manager = DatabaseManager(db_path)
    qs = QuestionService()
    # print(qs.get_filter_names())
    with db_manager.get_session() as session:
        # res = qr.get_questions_with_code(session, 10)
        # print(qs.get_all_options(session))
        questions = qs.get_questions_with_code(session, "abcd", True)

    print(questions)
