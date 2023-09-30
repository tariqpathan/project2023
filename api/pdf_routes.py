import shutil
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
from typing import Dict, Any

from test_generator.question_pdf_creator import generate_pdf
from test_generator.question_service import QuestionService
from api.dependencies import db_manager

pdf_router = APIRouter(
    dependencies=[Depends(db_manager.get_session)])

class PDFGenerator:
    def generate_pdf_wrapper(self, data: Dict[str, Any], file_name: str) -> None:
        generate_pdf(data, file_name)

def get_db():
    with db_manager.get_session() as db:
        try:
            yield db
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting data: {e}")


@pdf_router.get("/generate")
async def generate_pdf_route(
    pdf_generator: PDFGenerator = Depends(PDFGenerator),
    db_session: Session = Depends(get_db)):
    
    # Get data from QuestionService
    data = QuestionService.generate_questions(db_session, num_questions=8, answers=True)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_generator.generate_pdf_wrapper(data, tmp_file.name)

        tmp_file.seek(0)
        return FileResponse(tmp_file.name, headers={"Content-Disposition": "attachment; filename=example.pdf"})


@pdf_router.get("/generate/{code}")
async def generate_pdf_route_with_code(
    code: str,
    pdf_generator: PDFGenerator = Depends(PDFGenerator),
    db_session: Session = Depends(get_db)
):
    # Get data from QuestionService, changed 'code: int=code_str' to 'code=code'
    data = QuestionService.get_questions_with_code(db_session, code_str=code, answers=True)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf_generator.generate_pdf_wrapper(data, tmp_file.name)

        tmp_file.seek(0)
        return FileResponse(tmp_file.name, headers={"Content-Disposition": "attachment; filename=example.pdf"})



def setup_pdf_routes(app):
    app.include_router(pdf_router, prefix="/api/pdf")
