from typing import Optional
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    email: str
    # WARNING: you should have a email verification system in the app
    pwd_hash: str = Field(
        ...
    )  # NOTE: is the length here needed? maybe I should add the length verification in the app


class RegisterResponse(BaseModel):
    success: bool
    msg: str


class LoginRequest(BaseModel):
    name_or_email: str = Field(...)
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


class LogoutRequest(BaseModel):
    old_token: str


class LogoutResponse(BaseModel):
    success: bool
    msg: str


class GetUserProfileRequest(BaseModel):
    token: str


class GetUserProfileResponse(BaseModel):
    success: bool
    msg: str
    name: str
    email: str


class ChangePasswordRequest(BaseModel):
    name_or_email: str = Field(...)
    old_pwd_hash: str = Field(...)
    new_pwd_hash: str = Field(...)


class ChangePasswordResponse(BaseModel):
    success: bool
    msg: str
