from pydantic import BaseModel, Field, EmailStr, field_validator,ConfigDict

class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=8, max_length=15)

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

        model_config = ConfigDict(from_attributes=True)

class UserSingleResponse(BaseModel):
        data: UserResponse
        message:str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)

class UserLoginResponse(BaseModel):
    data: TokenResponse
    message: str