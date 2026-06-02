from fastapi import FastAPI

from src.web.routes import router

app = FastAPI(
    title="API Automação SEFAZ",
    version="0.1.0",
)

app.include_router(router)