from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

import extraction_engine.extract as extract


class ExtractionRequest(BaseModel):
    question_paper: str
    answer_paper: str
    exam_format: str


post_router = APIRouter(dependencies=[])


# TODO: Complete
@post_router.post("/extract/")
def initiate_extraction(request: ExtractionRequest):
    try:
        status = extract.run_extraction(request.exam_format, request.question_paper, request.answer_paper)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success" if status == 0 else "failed"}


def setup_post_routes(app):
    app.include_router(post_router, prefix="/api")


"""
    Fetch the list of available papers and populate a dropdown or list element.
    Fetch the list of available exam formats and populate a dropdown.
    Provide a button to initiate the extraction, which, when clicked, 
    gathers the selected values and makes a POST request to the /extract/ API endpoint.

"""
