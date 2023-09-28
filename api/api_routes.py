import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from database.models import Exam, Question, Subject, Subtopic, Difficulty
import database.database_utils as db_utils
from api.dependencies import db_manager, uploads_path, load_exam_formats



api_router = APIRouter(
    dependencies=[Depends(db_manager.get_session)]
)

def get_db():
    with db_manager.get_session() as db:
        try:
            yield db
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting data: {e}")

@api_router.get("/subjects/")
def get_all_subject(db_session: Session = Depends(get_db)):
    return db_utils.get_all_subjects(db_session)

@api_router.get("/subtopics/")
def get_all_subtopics(db_session: Session = Depends(get_db)):
    return db_utils.get_all_subtopics(db_session)

@api_router.get("/difficulties/")
def get_all_difficulties(db_session: Session = Depends(get_db)):
    return db_utils.get_all_difficulties(db_session)

@api_router.get("/subtopics/{subject_name}")
def get_subtopics_for_subject(subject_name: str, db_session: Session = Depends(get_db)):
    subject_id = db_utils.get_subject_id(db_session, subject_name)
    if not subject_id:
        raise HTTPException(status_code=404, detail=f"Subject with name {subject_name} does not exist.")
    return db_utils.get_subtopic_for_subject(db_session, subject_id)

@api_router.get("/examformats/")
def get_exam_formats():
    return load_exam_formats()

@api_router.get("/listfiles/")
def list_files():
    pdf_files = [f.name for f in Path(uploads_path).glob("*.pdf")]
    return {"files": pdf_files}

def setup_get_routes(app):
    app.include_router(api_router, prefix="/api")

