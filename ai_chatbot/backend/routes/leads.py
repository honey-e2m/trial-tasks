from fastapi import APIRouter
from models import LeadCreate, LeadResponse
from memory_store import leads

router = APIRouter()

@router.post("/", response_model=LeadResponse)
def create_lead(lead: LeadCreate):
    data = {"name": lead.name, "email": lead.email}
    leads.append(data)
    return data
