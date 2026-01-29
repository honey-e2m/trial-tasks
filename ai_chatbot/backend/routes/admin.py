from fastapi import APIRouter
from memory_store import leads

router = APIRouter()

@router.get("/stats")
def get_stats():
    return {"total_leads": len(leads)}
