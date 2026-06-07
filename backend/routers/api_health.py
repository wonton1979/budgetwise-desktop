from fastapi import APIRouter

router = APIRouter()

@router.get("/api/api_health")
def api_health():
    return {"status": "ok"}