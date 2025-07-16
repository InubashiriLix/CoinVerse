from os import access
from secrets import token_bytes
from typing import Optional

# fast api
from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

# fastapi response model
from fastapi_req_resp_type import RegisterRequest, RegisterResponse
from fastapi_req_resp_type import LoginRequest, LoginResponse, RefreshTokenResponse
from fastapi_req_resp_type import (
    RefreshTokenRequest,
    UserProfile,
    ChangePasswordRequest,
)

# the databse shits
from sqlite3 import Connection, IntegrityError
from db_api import init
from db_api import Account, AccountBook, Transaction

# the custom exceptions
from cus_exceptions import TokenExpireException, PwdNotMatchError

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(name)s - %(levelname)s] - %(message)s",
)

conn, _ = init()

router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


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
    if data.name is None and data.email is None:
        return LoginResponse(
            success=False, msg="name or email is required", access_token=None
        )
    # NOTE: the msg content is desired to be shown in the app, cause' it has the helpful hints
    try:
        temp_acc = Account.login(
            conn=conn,
            name_or_email=data.name if data.name is not None else data.email,  # pyright: ignore[reportArgumentType] # it has been checked before this line
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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="logout, invalidate the token",
)
async def logout():
    # TODO: invalidate the token
    pass


@router.get("/users/me", response_model=UserProfile, summary="get the user info")
async def get_profile():
    # Depends(get_current_user):
    # TODO: get the current user and return ther profile
    pass


@router.put(
    "/users/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="change the user password",
)
async def change_password():
    # TODO: change the user password here
    pass


app = FastAPI(title="shit", version="0.1.0")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fast_router:app", host="127.0.0.1", port=8000, reload=True)
