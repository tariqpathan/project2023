from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel


from test_generator.question_service import QuestionService
from api.dependencies import db_manager

question_router = APIRouter(
    dependencies=[Depends(db_manager.get_session)])


def get_db():
    with db_manager.get_session() as db:
        try:
            yield db
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting data: {e}")


@question_router.get("/random")
def get_random_questions(db_session: Session = Depends(get_db)):
    return QuestionService.generate_questions(db_session, 10)


@question_router.get("/code/{code}")
def get_questions_from_code(code: str, db_session: Session = Depends(get_db)):
    return QuestionService.get_questions_with_code(db_session, code, True)

class ResponseItem(BaseModel):
    question_id: int
    response: str

@question_router.post("/code/{code}")
def submit_answers(code: str, answers: list[ResponseItem], db_session: Session = Depends(get_db)):
    return None
    # return QuestionService.submit_answers(db_session, code, answers) #TODO


def setup_question_routes(app):
    app.include_router(question_router, prefix="/api/questions")
