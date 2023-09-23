from typing import Dict, List, Optional
from database.models import Answer, Question
from extraction_engine.factories.answer_factory import AnswerFactory
from extraction_engine.processing.CambridgeScienceAnswerProcessor import CambridgeScienceAnswerProcessor
from extraction_engine.processing.AbstractAnswerProcessor import AbstractAnswerProcessor


class AnswerManager:
    def __init__(self, exam_format: str) -> None:
        self.exam_format = exam_format
        self.answer_processor = self._get_answer_processor()
        self.answer_factory = None
    
    def _get_answer_processor(self) -> AbstractAnswerProcessor:
        """Returns an instance of the required answer processor based on exam board."""
        return AnswerProcessorFactory.create_processor(self.exam_format)
    
    def _set_answer_factory(self, db_session) -> None:
        """Returns an instance of the required answer factory based on exam board."""
        self.answer_factory = AnswerFactory(db_session)

    def execute(self, db_session, text: str, questions: List[Question]) -> None:
        self._set_answer_factory(db_session)
        answers = self.answer_processor.process(text)
        if not answers:
            print("No answers found in the provided text.")
            return
        self._match_questions(answers, questions)

    def _match_questions(self, qnum_answer_dict: Dict[int, str], questions: List[Question]):
        """Matches questions to their respective answers."""
        question_map = {q.question_number: q for q in questions}

        for qnum, answer_text in qnum_answer_dict.items():
            question = question_map.get(qnum)
            if not question:
                print(f"No matching question for qnum: {qnum}")
                continue
            # Create a new Answer object and associate it with the question
            if self.answer_factory: self.answer_factory.create_answer(question, answer_text)


class AnswerProcessorFactory:
    @staticmethod
    def create_processor(exam_format: str) -> AbstractAnswerProcessor:
        # A dictionary to map EXAM_FORMAT values to their respective classes
        processor_map = {
            "cambridge_science": CambridgeScienceAnswerProcessor,
        }
        # Fetch the appropriate class based on the exam_format string
        processor_class = processor_map.get(exam_format)
        
        if not processor_class:
            raise ValueError(f"No processor found for exam board '{exam_format}'")
        else:
            return processor_class()
