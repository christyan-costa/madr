import html
import re
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from madr.settings import Settings

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


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
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )

    return encoded_jwt
