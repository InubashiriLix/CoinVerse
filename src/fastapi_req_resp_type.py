from typing import Optional, List, Dict, Tuple
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


class CreateAccountBookRequest(BaseModel):
    token: str = Field(...)
    book_name: str = Field(...)


class CreateAccountBookResponse(BaseModel):
    """
    Attributes:
        success: the ops status
        code:
            # 0: success
            # 1: token lost
            # 2: token expired
            # 3. book name duplicated
        msg: information about the operation
    """

    success: bool = Field(...)
    code: int = Field(...)
    msg: str = Field(...)


class ListBookRequest(BaseModel):
    token: str = Field(...)


class ListBookResponse(BaseModel):
    """
    Attributes:
        success: the ops status
        code:
            # 0 success
            # 1 token lost
            # 2 token expired
        msg: info ops
        books: list of books
    """

    success: bool = Field(...)
    code: int = Field(...)
    msg: str = Field(...)
    books: List[Dict[int, Tuple[str, float]]]


class RemoveBookRequest(BaseModel):
    token: str = Field(...)
    book_id: int = Field(...)


class RemoveBookResponse(BaseModel):
    """
    Attributes:
        success: the ops status
        code:
            # 0 success
            # 1 token lost
            # 2 token expired
        msg: info ops
    """

    success: bool = Field(...)
    code: int = Field(...)
    msg: str = Field(...)


class BookDetailRequest(BaseModel):
    token: str = Field(...)
    account_book_id: int
    start_time: str = Field(...)
    end_time: str = Field(...)
    note: str = Field(...)


class BookDetailResponse(BaseModel):
    """
    Attributes:
        success: status
        code:
            # 0 success
            # 1 invlaid start_time or end time
            # 2 token lost
            # 3 token expired
            # 4 unkown
        transactions: [TODO:attribute]
    """

    success: bool = Field(...)
    msg: str = Field(...)
    code: int = Field(...)
    transactions: List[Dict[int, Tuple[str, str, float]]]


class AddIncomeRequest(BaseModel):
    token: str = Field(...)
    account_book_id: int = Field(...)
    amount: float = Field(...)
    time: str = Field(...)
    note: str = Field(...)
    income_idx: int = Field(...)


class AddIncomeResponse(BaseModel):
    """
    Attributes:
        success: [TODO:attribute]
        msg: [TODO:attribute]
        code:
            # 0 success
            # 1 invalid time str format
            # 2 requireInfo lost (useless
            # 3 token lost
            # 4 token expired
            # 5 unkown
    """

    success: bool = Field(...)
    msg: str = Field(...)
    code: int = Field(...)


class AddOutcomeRequest(BaseModel):
    token: str = Field(...)
    account_book_id: int = Field(...)
    amount: float = Field(...)
    time: str = Field(...)
    note: str = Field(...)
    outcome_idx: int = Field(...)


class AddOutcomeResponse(BaseModel):
    """
    Attributes:
        success: [TODO:attribute]
        msg: [TODO:attribute]
        code:
            # 0 success
            # 1 invalid time str format
            # 2 token lost
            # 3 token expired
            # 4 unkown
    """

    success: bool = Field(...)
    msg: str = Field(...)
    code: int = Field(...)


# NOTE: may be I should have a ops praraphase to the app so that it can have a more collective operation
