from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel


from test_generator.question_service import QuestionService
from api.dependencies import db_manager

question_router = APIRouter(
    dependencies=[Depends(db_manager.get_session)])

class ResponseItem(BaseModel):
    question_id: int
    response: str

def get_db():
    with db_manager.get_session() as db:
        try:
            yield db
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting data: {e}")


def evaluate_answers(db_session: Session, code: str, submtd_ansr: list[ResponseItem]) -> dict:
    data = QuestionService.get_questions_with_code(db_session, code)
    if data['code'] is None:
        raise HTTPException(status_code=404, detail="Code not found")
    
    actual_answers = {q['id']: q['answer'] for q in data['result']}
    submitted_answers = {q.question_id: q.response for q in submtd_ansr}

    actual_ids = set(actual_answers.keys())
    submitted_ids = set(submitted_answers.keys())
    valid_ids = actual_ids.intersection(submitted_ids)

    # Identify correct, wrong, and invalid IDs
    correct_answers = [id for id in valid_ids if submitted_answers[id] == actual_answers[id]]
    wrong_answers = [id for id in valid_ids if submitted_answers[id] != actual_answers[id]]
    invalid_ids = submitted_ids.difference(valid_ids)
    score = len(correct_answers)
    
    return {
        'score': score,
        'total': len(actual_ids),
        'correct_answers': correct_answers,
        'wrong_answers': wrong_answers,
        'invalid_ids': invalid_ids,
    }


@question_router.get("/random")
def get_random_questions(db_session: Session = Depends(get_db)):
    return QuestionService.generate_questions(db_session, 10)


@question_router.get("/code/{code}")
def get_questions_from_code(code: str, db_session: Session = Depends(get_db)):
    return QuestionService.get_questions_with_code(db_session, code, True)

@question_router.post("/code/{code}")
def submit_answers_route(code: str, request: list[ResponseItem], db_session: Session = Depends(get_db)):
    return evaluate_answers(db_session, code, request)


def setup_question_routes(app):
    app.include_router(question_router, prefix="/api/questions")
