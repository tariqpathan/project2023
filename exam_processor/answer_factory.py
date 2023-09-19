from database.models import Answer, Question

class AnswerFactory:
    def __init__(self, db_session) -> None:
        self.db_session = db_session
    
    def create_answer(self, question: Question, correct_answer: str) -> Answer:
        """creates an answer object using the Answer model"""
        answer = Answer(question_id=question.id, answer=correct_answer)
        try:
            self.db_session.add(answer)
        except Exception as e:
            raise Exception(f"Error creating Answer: {answer}. Error: {e}")
        return answer
