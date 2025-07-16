from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    pwd_hash: str = Field(
        ...
    )  # NOTE: is the length here needed? maybe I should add the length verification in the app


class RegisterResponse(BaseModel):
    success: bool
    msg: str


class LoginRequest(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    pwd_hash: str = Field(
        ...
    )  # NOTE: same as the note in the class RegisterRequest pwd_hash
    maintain_online: bool = Field(...)


class LoginResponse(BaseModel):
    success: bool
    msg: str
    token_type: str = "bearer"
    access_token: Optional[str]


class RefreshTokenResponse(BaseModel):
    sucess: bool
    expired: bool
    msg: str
    access_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    old_token: str


class UserProfile(BaseModel):
    name: str
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    pwd_hash: str = Field(...)
