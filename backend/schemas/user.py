from pydantic import BaseModel, Field, EmailStr, field_validator,ConfigDict

from backend.models.currency_type import CurrencyType
from backend.models.date_format_type import DateFormatType


class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=8, max_length=15)
    family_code: str

    @field_validator("password")
    def validate_password(cls, v):
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v


class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
        username: str
        email: EmailStr
        display_name: str
        family_code: str
        preferred_date_format: DateFormatType
        preferred_currency_display: CurrencyType
        model_config = ConfigDict(from_attributes=True)

class UserSingleResponse(BaseModel):
        data: UserResponse
        message:str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserLoginResponse(BaseModel):
    data: TokenResponse
    message: str

class UserUpdateProfile(BaseModel):
    display_name: str | None = None
    preferred_currency_display : CurrencyType | None = None
    preferred_date_format : DateFormatType | None = None