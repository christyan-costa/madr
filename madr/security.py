import html
import re
from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, decode, encode
from jwt.exceptions import PyJWKError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from madr.database import get_session
from madr.models import User
from madr.schemas import TokenData
from madr.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
settings = Settings()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def sanitize_string(input_string: str) -> str:
    # Step 1: Strip leading/trailing whitespace
    sanitized = input_string.strip()

    # Step 2: Remove unwanted characters
    sanitized = re.sub(
        r'[^a-zA-Z0-9 .,\'\"@#&()\-ÁáÂâÃãÀàÉéÊêÍíÓóÔôÕõÚúÇç]', '', sanitized
    )
    # Step 3: Replace sequences of whitespace (tabs, newlines)
    # with a single space
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Step 4: Escape HTML special characters to prevent XSS attacks
    sanitized = html.escape(sanitized)

    # Step 5: Put string into lowercase format
    sanitized = sanitized.lower()

    return sanitized


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get('sub')
        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise credentials_exception
    except PyJWKError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user:
        raise credentials_exception

    return user
