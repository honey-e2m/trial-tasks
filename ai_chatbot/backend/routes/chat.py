from fastapi import APIRouter
from models import ChatRequest, ChatResponse
from rag_service import get_answer

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    # TODO: Log chat to Supabase 'chats' table if needed
    
    answer = get_answer(request.message)
    return ChatResponse(answer=answer, sources=["e2msolutions.com"])
