from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LeadCreate(BaseModel):
    name: str
    email: str

class LeadResponse(LeadCreate):
    id: Optional[str] = None
    created_at: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    lead_id: Optional[str] = None  # Optional: Link chat to a lead

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []

class AdminStats(BaseModel):
    total_leads: int
    total_chats: int
