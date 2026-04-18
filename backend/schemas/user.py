from pydantic import BaseModel, Field, EmailStr, field_validator

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

class UserResponse(BaseModel):
        username: str
        email: EmailStr

class UserSingleResponse(BaseModel):
        data: UserResponse
        message:str