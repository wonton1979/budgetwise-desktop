from fastapi import APIRouter
from backend.schemas.user import UserCreate, UserSingleResponse, UserLogin, UserLoginResponse
from backend.services.user_service import add_user,login_user_service

router = APIRouter()

@router.post("/users",response_model=UserSingleResponse)
def create_user(user: UserCreate):
    return {
        "data":add_user(user),
        "message":"User created"
    }

@router.post("/users/login",response_model=UserLoginResponse)
def login_user(user: UserLogin):
    return {
        "data":login_user_service(user),
        "message":"User logged in"
    }
