from fastapi import APIRouter
from backend.schemas.user import UserCreate, UserSingleResponse, TokenResponse, UserUpdateProfile
from backend.services.user_service import add_user, login_user_service, fetch_current_user, update_user_profile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()


def get_current_user(token: str = Depends(oauth2_scheme)):
    current_user = fetch_current_user(token)
    return current_user

@router.post("/api/auth/register",response_model=UserSingleResponse)
def create_user(user: UserCreate):
    return {
        "data":add_user(user),
        "message":"User created"
    }

@router.post("/api/auth/login",response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user_service(form_data.username,form_data.password)


@router.get("/api/auth/me",response_model=UserSingleResponse)
def get_me(token: str = Depends(oauth2_scheme)):
    response = get_current_user(token)
    return {
        "data": {
            "username": response.username,
            "email": response.email,
            "family_code": response.family_code,
            "display_name": response.display_name,
            "preferred_date_format": response.preferred_date_format,
            "preferred_currency_display": response.preferred_currency_display,
        },
        "message":"Current User Information"
    }

@router.patch("/api/auth/me")
def update_me_profile(updated_user_profile:UserUpdateProfile, current_user = Depends(get_current_user)):
    response = update_user_profile(updated_user_profile, current_user.id)
    return response