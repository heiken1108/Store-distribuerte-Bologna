from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Weather Forecast Service")

app.include_router(router)