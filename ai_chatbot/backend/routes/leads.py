from fastapi import APIRouter, HTTPException
from models import LeadCreate, LeadResponse
from database import supabase

router = APIRouter()

@router.post("/", response_model=LeadResponse)
def create_lead(lead: LeadCreate):
    data = {"name": lead.name, "email": lead.email}
    response = supabase.table("leads").insert(data).execute()
    
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create lead")
        
    return response.data[0]
