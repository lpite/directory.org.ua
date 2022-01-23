from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from directory import territories

app = FastAPI(openapi_url='/api/openapi.json', docs_url='/api')

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(territories.api.router)
app.include_router(territories.views.router)
