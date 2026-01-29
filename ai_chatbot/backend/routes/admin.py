from fastapi import APIRouter
from database import supabase

router = APIRouter()

@router.get("/stats")
def get_stats():
    leads_count = supabase.table("leads").select("*", count="exact").execute().count
    # Note: 'chats' table logic would go here
    return {"total_leads": leads_count}
