from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException

class ExtractionRequest(BaseModel):
    question_paper: str
    answer_paper: str
    exam_format: str


post_router = APIRouter(
    dependencies = []
)

# TODO: Complete
@post_router.post("/extract/")
def initiate_extraction(request: ExtractionRequest):
    # Logic to start the extraction process
    # Use request.question_paper, request.answer_paper, and request.exam_format
    return {"status": "Extraction initiated"}

@post_router.get("/status/")
def get_extraction_status():
    return {"status": "TODO"}

def setup_post_routes(app):
    app.include_router(post_router, prefix="/api")