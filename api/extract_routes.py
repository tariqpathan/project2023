from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

import extraction_engine.extract as extract


class ExtractionRequest(BaseModel):
    question_paper: str
    answer_paper: str
    exam_format: str


extract_router = APIRouter(dependencies=[])


@extract_router.post("/extract/")
def initiate_extraction(request: ExtractionRequest):
    try:
        status = extract.run_extraction(request.exam_format, request.question_paper, request.answer_paper)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success" if status == 0 else "failed"}


def setup_extract_routes(app):
    app.include_router(extract_router, prefix="/api")
