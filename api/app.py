from fastapi import FastAPI
from api.general_routes import setup_general_routes
from api.extract_routes import setup_extract_routes
from api.question_routes import setup_question_routes
from api.pdf_routes import setup_pdf_routes


app = FastAPI()
setup_general_routes(app)
setup_extract_routes(app)
setup_question_routes(app)
setup_pdf_routes(app)
