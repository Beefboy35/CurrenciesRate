
from fastapi import FastAPI
from uvicorn import run

from src.api.endpoints.users import api
from src.auth.auth import reg
from src.utils.external_api.routes import ext_api

app = FastAPI()
app.include_router(reg)
app.include_router(api)
app.include_router(ext_api)

if __name__ == "__main__":
    run("main:app", host="localhost", port=8000, reload=True)