from typing import Optional

# fast api
from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

# fastapi response model
from fastapi_req_resp_type import (
    ChangePasswordResponse,
    RegisterRequest,
    RegisterResponse,
)
from fastapi_req_resp_type import LoginRequest, LoginResponse, RefreshTokenResponse
from fastapi_req_resp_type import (
    RefreshTokenRequest,
    GetUserProfileRequest,
    GetUserProfileResponse,
    ChangePasswordRequest,
)
from fastapi_req_resp_type import LogoutRequest, LogoutResponse

# the databse shits
from sqlite3 import Connection, IntegrityError
from db_api import init
from db_api import Account, AccountBook, Transaction

# the custom exceptions
from cus_exceptions import (
    RequireInfoLostException,
    TokenExpireException,
    PwdNotMatchError,
    TokenNotFoundError,
)

import logging

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
async def register_user(data: RegisterRequest):
    try:
        Account.register(conn, name=data.name, email=data.email, pwd_hash=data.pwd_hash)
        logging.info(f"User {data.name} registered successfully.")
        return RegisterResponse(success=True, msg="User registered successfully.")
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
async def login(data: LoginRequest):
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
async def refresh_token(data: RefreshTokenRequest):
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
async def logout(data: LogoutRequest):
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
async def get_profile(data: GetUserProfileRequest):
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
    "/users/me/password",
    response_model=ChangePasswordResponse,
    summary="change the user password",
)
async def change_password(data: ChangePasswordRequest):
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
    except RequireInfoLostException as e:
        logging.warning(f"Require info lost: {e}")
        return ChangePasswordResponse(success=False, msg=str(e))
    except PwdNotMatchError:
        logging.warning("Old password does not match")
        return ChangePasswordResponse(success=False, msg="Old password does not match")
    except Exception as e:
        logging.error(f"Error changing password: {e}")
        return ChangePasswordResponse(success=False, msg=str(e))


app = FastAPI(title="CoinVerse", version="0.1.0")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fast_router:app", host="127.0.0.1", port=8000, reload=True)
