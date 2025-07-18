from datetime import datetime

# fast api
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, status

# fastapi response model
from fastapi_req_resp_type import (
    AddIncomeRequest,
    AddIncomeResponse,
    AddOutcomeRequest,
    AddOutcomeResponse,
    BookDetailResponse,
    BookDetailRequest,
    ChangePasswordResponse,
    CreateAccountBookRequest,
    CreateAccountBookResponse,
    RemoveBookRequest,
    RemoveBookResponse,
    ListBookRequest,
    ListBookResponse,
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenResponse,
    RefreshTokenRequest,
    GetUserProfileRequest,
    GetUserProfileResponse,
    ChangePasswordRequest,
    LogoutRequest,
    LogoutResponse,
)

# the databse shits
from sqlite3 import Connection, IntegrityError
from db_api import Account, AccountBook, Transaction, init
from db_api import IncomeType, OutcomeType

# the custom exceptions
from cus_exceptions import (
    LoginFailedError,
    DuplicatedAccountBookError,
    EmailFormatError,
    IncomeTypeIndexError,
    IncomeValueError,
    InvalidOutcomeIncomeValueError,
    OutcomeTypeIndexError,
    OutcomeValueError,
    PasswordWrongError,
    RequireInfoLostException,
    TimeFormatError,
    TokenExpireException,
    PwdNotMatchError,
    TokenNotFoundError,
    AccessDenialAccountBookError,
)

import logging

from utils import verify_email_format, str_to_datetime

from typing import Dict, Type
from fastapi.responses import JSONResponse
from fastapi import Request

# 1️⃣  把所有自定义异常 → code 映射集中在这里
EXC_CODE_MAP: Dict[Type[Exception], int] = {
    EmailFormatError: 1001,
    IntegrityError: 1002,
    PwdNotMatchError: 1003,
    TokenExpireException: 1004,
    TokenNotFoundError: 1005,
    RequireInfoLostException: 1006,
    PasswordWrongError: 1007,
    DuplicatedAccountBookError: 1008,
    TimeFormatError: 1009,
    IncomeValueError: 1010,
    IncomeTypeIndexError: 1011,
    OutcomeValueError: 1012,
    OutcomeTypeIndexError: 1013,
    InvalidOutcomeIncomeValueError: 1014,
    LoginFailedError: 1015,
    AccessDenialAccountBookError: 1016,
    # ……需要时继续往下加
}

DEFAULT_ERR_CODE = 1999  # 未知异常统一用这个编号

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(name)s - %(levelname)s] - %(message)s",
)

conn: Connection
conn, _ = init()

router: APIRouter = APIRouter(prefix="/CoinVerse", tags=["interfaces"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="create new user account",
)
async def register_user(data: RegisterRequest) -> RegisterResponse:
    Account.register(conn, name=data.name, email=data.email, pwd_hash=data.pwd_hash)
    logging.info(f"User {data.name} registered successfully.")
    return RegisterResponse(success=True, msg="User registered successfully.")


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="name / email + pwd to login, return the token",
)
async def login(data: LoginRequest) -> LoginResponse:
    temp_acc = Account.login(
        conn=conn,
        name_or_email=data.name_or_email,
        pwd_hash=data.pwd_hash,
    )
    if temp_acc is None:
        logging.error("Login failed, unkown error: returned Account is None")
        raise LoginFailedError("login failed, unknown error with Account is None")
    return LoginResponse(
        success=True, msg="Login successful", access_token=temp_acc.token
    )


@router.post(
    "/refresh_token", response_model=RefreshTokenResponse, summary="refresh the token"
)
async def refresh_token(data: RefreshTokenRequest) -> RefreshTokenResponse:
    temp_acc = Account.refresh_token(conn=conn, old_token=data.old_token)
    if temp_acc is None:
        raise TokenExpireException(
            "Invalid or expired token",
        )
    return RefreshTokenResponse(
        sucess=True,
        expired=False,
        access_token=temp_acc.token,
        msg="successfully update the token",
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="logout, invalidate the token (expire it)",
)
async def logout(data: LogoutRequest) -> LogoutResponse:
    status = Account.logout(conn=conn, token=data.old_token)
    return LogoutResponse(
        success=status, msg="Logout successful" if status else "Logout failed"
    )


@router.post(
    "/users/me", response_model=GetUserProfileResponse, summary="get the user info"
)
async def get_profile(data: GetUserProfileRequest) -> GetUserProfileResponse:
    temp_account = Account.get_profile(conn=conn, token=data.token)
    return GetUserProfileResponse(
        success=True,
        msg="Profile retrieved successfully",
        name=temp_account.name,
        email=temp_account.email,
    )


@router.put(
    "/users/me/change_password",
    response_model=ChangePasswordResponse,
    summary="change the user password",
)
async def change_password(data: ChangePasswordRequest) -> ChangePasswordResponse:
    if data.old_pwd_hash == data.new_pwd_hash:
        logging.warning("Old password and new password are the same")
        return ChangePasswordResponse(
            success=False, msg="Old password and new password cannot be the same"
        )
    Account.change_pwd(
        conn=conn,
        email_or_name=data.name_or_email,  # pyright: ignore[reportArgumentType] # it has been checked before this line
        old_pwd_hash=data.old_pwd_hash,
        new_pwd_hash=data.new_pwd_hash,
    )
    return ChangePasswordResponse(success=True, msg="Password changed successfully")


@router.post(
    "/create_book",
    response_model=CreateAccountBookResponse,
    summary="create a new account book (need token)",
)
async def create_acc_book(data: CreateAccountBookRequest) -> CreateAccountBookResponse:
    Account.create_book(conn=conn, token=data.token, book_name=data.book_name)
    return CreateAccountBookResponse(
        success=True, code=0, msg="Book created successfully"
    )


@router.put(
    "/list_books",
    response_model=ListBookResponse,
    summary="list the books in the account (need token)",
)
async def list_acc_book(data: ListBookRequest) -> ListBookResponse:
    temp_acc_books_list = Account.list_books(conn=conn, token=data.token)
    if len(temp_acc_books_list) == 0:
        logging.info("No books found for the account")
        return ListBookResponse(success=True, code=0, msg="No books found", books=[])

    else:
        return ListBookResponse(
            success=True,
            code=0,
            msg="Books found",
            books=[
                {
                    single_book._id: (
                        single_book.name,
                        single_book.get_balance(conn=conn),
                    )
                }
                for single_book in temp_acc_books_list
            ],
        )


@router.post(
    "/books/remove_book",
    response_model=RemoveBookResponse,
    summary="remove the book by book_id (need token)",
)
async def remove_book(data: RemoveBookRequest) -> RemoveBookResponse:
    Account.remove_account_book(conn=conn, token=data.token, book_id=data.book_id)
    return RemoveBookResponse(success=True, code=0, msg="Book removed successfully")


@router.post(
    "/books_detail",
    response_model=BookDetailResponse,
    summary="get the book detail by book_id (need token)",
)
async def get_book_detail(data: BookDetailRequest) -> BookDetailResponse:
    temp_start_time = (
        str_to_datetime(data.start_time) if len(data.start_time) > 1 else datetime.now()
    )
    temp_end_time = (
        str_to_datetime(data.end_time) if len(data.end_time) > 1 else datetime.now()
    )

    temp_note = None if len(data.note) == 0 else data.note
    temp = AccountBook.get_transaction_list(
        conn=conn,
        token=data.token,
        account_book_id=data.account_book_id,
        start_time=temp_start_time,
        end_time=temp_end_time,
        note=temp_note,
    )
    return BookDetailResponse(
        success=True,
        code=0,
        msg="Success",
        transactions=[
            {tx.id: (str(tx.category.name), tx.note, tx.amount)}
            for tx in temp
            if tx.id is not None and tx.category is not None
        ],
    )


@router.post(
    "/book/transactions/add_income",
    response_model=AddIncomeResponse,
    summary="add a transaction to the book (need token)",
)
async def add_income(data: AddIncomeRequest):
    if len(data.time) > 1:
        temp = data.time
    else:
        temp = datetime.now().isoformat()
    AccountBook.add_income(
        conn=conn,
        account_book_id=data.account_book_id,
        token=data.token,
        amount=data.amount,
        time=str_to_datetime(temp),
        note=data.note,
        income_type=IncomeType.index_2_income_type(data.income_idx),
    )
    return AddIncomeResponse(success=True, msg="Income added successfully", code=0)


@router.post(
    "/book/transactions/add_outcome",
    response_model=AddOutcomeResponse,
    summary="add a transaction to the book (need token)",
)
async def add_outcome(data: AddOutcomeRequest) -> AddOutcomeResponse:
    if len(data.time) > 1:
        temp = data.time
    else:
        temp = datetime.now().isoformat()
    AccountBook.add_outcome(
        conn=conn,
        account_book_id=data.account_book_id,
        token=data.token,
        amount=data.amount,
        time=str_to_datetime(temp),
        note=data.note,
        outcome_type=OutcomeType.index_2_outcome_type(data.outcome_idx),
    )
    return AddOutcomeResponse(success=True, msg="Outcome added successfully", code=0)


app = FastAPI(title="CoinVerse", version="0.1.0")
app.include_router(router)


@app.middleware("http")
async def global_exception_middleware(request: Request, call_next):
    """
    捕获业务层抛出的自定义异常：
      1. 命中 EXC_CODE_MAP → 返回 {success:false, code:..., msg:str(e)}
      2. 其它异常 → code=DEFAULT_ERR_CODE
    成功响应和 FastAPI 自带的 4xx/5xx 行为保持原样。
    """
    try:
        return await call_next(request)

    except tuple(EXC_CODE_MAP.keys()) as e:
        code = EXC_CODE_MAP[type(e)]
        logging.warning(f"[Handled] {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=200,  # 业务错误仍返回 200，前端靠 code 判断
            content={"success": False, "code": code, "msg": str(e)},
        )

    except Exception as e:
        logging.exception(f"[Unhandled] {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": DEFAULT_ERR_CODE,
                "msg": f"Internal Server Error: {e}",
            },
        )


# =======================================================================
if __name__ == "__main__":
    import uvicorn
    from db_api import delete_all

    delete_all()

    uvicorn.run("fast_router:app", host="127.0.0.1", port=8000, reload=True)
