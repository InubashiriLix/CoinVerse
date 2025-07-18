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
    DuplicatedAccountBookError,
    EmailFormatError,
    IncomeValueError,
    InvalidOutcomeIncomeValueError,
    OutcomeValueError,
    PasswordWrongError,
    RequireInfoLostException,
    TimeFormatError,
    TokenExpireException,
    PwdNotMatchError,
    TokenNotFoundError,
)

import logging

from utils import verify_email_format, str_to_datetime

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
    try:
        Account.register(conn, name=data.name, email=data.email, pwd_hash=data.pwd_hash)
        logging.info(f"User {data.name} registered successfully.")
        return RegisterResponse(success=True, msg="User registered successfully.")
    except EmailFormatError as e:
        logging.error(f"Error registering user {data.name}: {e}")
        return RegisterResponse(success=False, msg="Invalid email Format")
    except IntegrityError as e:
        logging.error(f"Error registering user {data.name}: {e}")
        return RegisterResponse(
            success=False, msg=str(e) + "\n consider if the account has been existed"
        )
    except Exception as e:
        logging.error(f"Error registering user {data.name}: {e}")
        return RegisterResponse(success=False, msg=str(e))


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="name / email + pwd to login, return the token",
)
async def login(data: LoginRequest) -> LoginResponse:
    try:
        temp_acc = Account.login(
            conn=conn,
            name_or_email=data.name_or_email,
            pwd_hash=data.pwd_hash,
        )
        if temp_acc is None:
            logging.error("Login failed, unkown error: returned Account is None")
            raise RuntimeError("login failed, unknown error with Account is None")
        return LoginResponse(
            success=True, msg="Login successful", access_token=temp_acc.token
        )
    except PwdNotMatchError:
        logging.warning("Password does not match")
        return LoginResponse(
            success=False, msg="Password does not match", access_token=None
        )
    except Exception as e:
        logging.error(f"Error logging in user: {e}")
        return LoginResponse(success=False, msg=str(e), access_token=None)


@router.post(
    "/refresh_token", response_model=RefreshTokenResponse, summary="refresh the token"
)
async def refresh_token(data: RefreshTokenRequest) -> RefreshTokenResponse:
    try:
        temp_acc = Account.refresh_token(conn=conn, old_token=data.old_token)
        if temp_acc is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        return RefreshTokenResponse(
            sucess=True,
            expired=False,
            access_token=temp_acc.token,
            msg="successfully update the token",
        )
    except TokenExpireException:
        logging.warning("Token expired, returning expired response")
        return RefreshTokenResponse(
            sucess=False,
            expired=True,
            access_token="",
            msg="Token expired, please login again",
        )
    except Exception as e:
        logging.error(f"Error refreshing token: {e}")
        return RefreshTokenResponse(
            sucess=False, expired=False, access_token="", msg=f"Unknown Erorr: {e}"
        )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="logout, invalidate the token (expire it)",
)
async def logout(data: LogoutRequest) -> LogoutResponse:
    try:
        status = Account.logout(conn=conn, token=data.old_token)
        return LogoutResponse(
            success=status, msg="Logout successful" if status else "Logout failed"
        )
    except TokenNotFoundError:
        logging.warning("Token not found, cannot logout")
        # NOTE: the True cause' protection programming?
        return LogoutResponse(success=True, msg="Token not found, cannot logout")
    except Exception as e:
        logging.error(f"Error logging out user: {e}")
        return LogoutResponse(success=False, msg=str(e))


@router.get(
    "/users/me", response_model=GetUserProfileResponse, summary="get the user info"
)
async def get_profile(data: GetUserProfileRequest) -> GetUserProfileResponse:
    try:
        Account.get_profile(conn=conn, token=data.token)
        return GetUserProfileResponse(
            success=True,
            msg="Profile retrieved successfully",
            name=Account.name,
            email=Account.email,
        )
    except TokenNotFoundError:
        logging.warning("Token not found, cannot get profile")
        return GetUserProfileResponse(
            success=False, msg="Token not found, cannot get profile", name="", email=""
        )
    except Exception as e:
        logging.error(f"Error getting user profile: {e}")
        return GetUserProfileResponse(success=False, msg=str(e), name="", email="")


@router.put(
    "/users/me/change_password",
    response_model=ChangePasswordResponse,
    summary="change the user password",
)
async def change_password(data: ChangePasswordRequest) -> ChangePasswordResponse:
    try:
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
    except PasswordWrongError as e:
        logging.warning(f"Password wrong: {e}")
        return ChangePasswordResponse(success=False, msg="Old password is incorrect")
    except RequireInfoLostException as e:
        logging.warning(f"Require info lost: {e}")
        return ChangePasswordResponse(success=False, msg=str(e))
    except PwdNotMatchError:
        logging.warning("Old password does not match")
        return ChangePasswordResponse(success=False, msg="Old password does not match")
    except Exception as e:
        logging.error(f"Error changing password: {e}")
        return ChangePasswordResponse(success=False, msg=str(e))


@router.post(
    "/create_book",
    response_model=CreateAccountBookResponse,
    summary="create a new account book (need token)",
)
async def create_acc_book(data: CreateAccountBookRequest) -> CreateAccountBookResponse:
    try:
        Account.create_book(conn=conn, token=data.token, book_name=data.book_name)
        return CreateAccountBookResponse(
            success=True, code=0, msg="Book created successfully"
        )
    except DuplicatedAccountBookError as e:
        logging.warning(f"Duplicated account book error: {e}")
        return CreateAccountBookResponse(
            success=False, code=3, msg="Duplicated book name"
        )
    except TokenNotFoundError as e:
        logging.warning(f"Token not found: {e}")
        return CreateAccountBookResponse(success=False, code=1, msg="Token not found")
    except TokenExpireException as e:
        logging.warning(f"Token expired: {e}")
        return CreateAccountBookResponse(
            success=False, code=2, msg="Token expired, please login again"
        )
    except RequireInfoLostException as e:
        logging.warning(f"Require info lost: {e}")
        return CreateAccountBookResponse(code=4, success=False, msg=str(e))
    except Exception as e:
        logging.error(f"Error creating account book: {e}")
        return CreateAccountBookResponse(success=False, code=5, msg=str(e))


@router.put(
    "/list_books",
    response_model=ListBookResponse,
    summary="list the books in the account (need token)",
)
async def list_acc_book(data: ListBookRequest) -> ListBookResponse:
    try:
        temp_acc_books_list = Account.list_books(conn=conn, token=data.token)
        if len(temp_acc_books_list) == 0:
            logging.info("No books found for the account")
            return ListBookResponse(
                success=True, code=0, msg="No books found", books=[]
            )

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
    except TokenNotFoundError as e:
        logging.warning(f"Token not found: {e}")
        return ListBookResponse(success=False, code=1, msg="Token not found", books=[])
    except TokenExpireException as e:
        logging.warning(f"Token expired: {e}")
        return ListBookResponse(
            success=False, code=2, msg="Token expired, please login again", books=[]
        )
    except Exception as e:
        logging.error(f"Error listing account books: {e}")
        return ListBookResponse(success=False, code=3, msg=str(e), books=[])


@router.post(
    "/books/remove_book",
    response_model=RemoveBookResponse,
    summary="remove the book by book_id (need token)",
)
async def remove_book(data: RemoveBookRequest) -> RemoveBookResponse:
    try:
        Account.remove_account_book(conn=conn, token=data.token, book_id=data.book_id)
        return RemoveBookResponse(success=True, code=0, msg="Book removed successfully")
    except TokenNotFoundError as e:
        logging.warning(f"Token not found: {e}")
        return RemoveBookResponse(success=False, code=1, msg="Token not found")
    except TokenExpireException as e:
        logging.warning(f"Token expired: {e}")
        return RemoveBookResponse(
            success=False, code=2, msg="Token expired, please login again"
        )
    except Exception as e:
        logging.error(f"Error listing account books: {e}")
        return RemoveBookResponse(success=False, code=3, msg=str(e))


@router.post(
    "/books_detail",
    response_model=BookDetailResponse,
    summary="get the book detail by book_id (need token)",
)
async def get_book_detail(data: BookDetailRequest) -> BookDetailResponse:
    try:
        try:
            temp_start_time = (
                None
                if len(data.start_time) == 0
                else datetime.fromisoformat(data.start_time)
            )
            temp_end_time = (
                None
                if len(data.end_time) == 0
                else datetime.fromisoformat(data.end_time)
            )
        except ValueError as e:
            logging.error(f"Invalid date format: {e}")
            return BookDetailResponse(
                success=False, code=1, msg="Invalid date format", transactions=[]
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

    except TokenNotFoundError as e:
        logging.warning(f"Token not found: {e}")
        return BookDetailResponse(
            success=False, code=2, msg="Token not found", transactions=[]
        )
    except TokenExpireException as e:
        logging.warning(f"Token expired: {e}")
        return BookDetailResponse(
            success=False,
            code=3,
            msg="Token expired, please login again",
            transactions=[],
        )
    except Exception as e:
        logging.error(f"Error getting book detail: {e}")
        return BookDetailResponse(success=False, code=4, msg=str(e), transactions=[])


@router.post(
    "book/transactions/add_income",
    response_model=AddIncomeResponse,
    summary="add a transaction to the book (need token)",
)
async def add_income(data: AddIncomeRequest):
    try:
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
    except TimeFormatError as e:
        logging.error(f"Time format error: {e}")
        return AddIncomeResponse(success=False, code=1, msg=str(e))
    except RequireInfoLostException as e:
        logging.warning(f"Require info lost: {e}")
        return AddIncomeResponse(success=False, code=2, msg=str(e))
    except TokenNotFoundError as e:
        logging.warning(f"Token not found: {e}")
        return AddIncomeResponse(success=False, code=3, msg="Token not found")
    except TokenExpireException as e:
        logging.warning(f"Token expired: {e}")
        return AddIncomeResponse(
            success=False, code=4, msg="Token expired, please login again"
        )
    except ValueError as e:
        logging.error(f"Invalid input time: {e}")
        return AddIncomeResponse(success=False, code=5, msg="Income Type Index Error")
    except Exception as e:
        logging.error(f"Error adding income: {e}")
        return AddIncomeResponse(success=False, code=6, msg=str(e))


@router.post(
    "book/transactions/add_outcome",
    response_model=AddOutcomeResponse,
    summary="add a transaction to the book (need token)",
)
async def add_outcome(data: AddOutcomeRequest) -> AddOutcomeResponse:
    try:
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
        return AddOutcomeResponse(
            success=True, msg="Outcome added successfully", code=0
        )
    except TimeFormatError as e:
        logging.error(f"Invalid input time: {e}")
        return AddOutcomeResponse(
            success=False, code=1, msg="Invalid input time format"
        )
    except TokenNotFoundError as e:
        logging.warning(f"Token not found: {e}")
        return AddOutcomeResponse(success=False, code=2, msg="Token not found")
    except TokenExpireException as e:
        logging.warning(f"Token expired: {e}")
        return AddOutcomeResponse(
            success=False, code=3, msg="Token expired, please login again"
        )
    except OutcomeValueError as e:
        logging.error(f"Invalid Outcome Value: {e}")
        return AddOutcomeResponse(success=False, code=4, msg=str(e))
    except InvalidOutcomeIncomeValueError as e:
        logging.exception(f"Invlaid Outcome Value: {e}")
        return AddOutcomeResponse(success=False, code=5, msg=str(e))
    except Exception as e:
        logging.exception(f"Error adding outcome: {e}")
        return AddOutcomeResponse(success=False, code=6, msg=str(e))


app = FastAPI(title="CoinVerse", version="0.1.0")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    from db_api import delete_all

    delete_all()

    uvicorn.run("fast_router:app", host="127.0.0.1", port=8000, reload=True)
