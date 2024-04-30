from fastapi import APIRouter

from app.ai.ai_response import get_response


router = APIRouter(prefix="/ai", tags=["Получение ответов"])

@router.get("")
def get_ai_response(q: str):
        return get_response(q)