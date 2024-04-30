from fastapi import FastAPI
from app.ai.router import router as ai_router

app = FastAPI()

app.include_router(ai_router)