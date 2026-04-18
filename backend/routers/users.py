from fastapi import APIRouter
from backend.schemas.user import UserCreate, UserSingleResponse, UserResponse
from backend.services.user_service import add_user

router = APIRouter()

@router.post("/users",response_model=UserSingleResponse)
def create_user(user: UserCreate):
    return {
        "data":add_user(user),
        "message":"User created"
    }