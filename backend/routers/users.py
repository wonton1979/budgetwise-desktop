from fastapi import APIRouter
from backend.schemas.user import UserCreate, UserSingleResponse, UserLogin, UserLoginResponse, TokenResponse
from backend.services.user_service import add_user,login_user_service,fetch_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
router = APIRouter()


def get_current_user(token: str = Depends(oauth2_scheme)):
    current_user = fetch_current_user(token)
    return current_user

@router.post("/users",response_model=UserSingleResponse)
def create_user(user: UserCreate):
    return {
        "data":add_user(user),
        "message":"User created"
    }

@router.post("/users/login",response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user_service(form_data.username,form_data.password)

