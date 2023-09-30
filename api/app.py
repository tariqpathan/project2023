from fastapi import FastAPI
from api.general_routes import setup_get_routes
from api.post_routes import setup_post_routes
from api.question_routes import setup_question_routes


app = FastAPI()
setup_get_routes(app)
setup_post_routes(app)
setup_question_routes(app)
