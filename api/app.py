from fastapi import FastAPI
from api.api_routes import setup_get_routes
from api.post_routes import setup_post_routes


app = FastAPI()
setup_get_routes(app)
setup_post_routes(app)
