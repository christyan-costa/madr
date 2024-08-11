import html
import re

from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def sanitize_string(input_string: str) -> str:
    """
    Sanitizes a string by removing or replacing unwanted characters,
    stripping whitespace, and escaping HTML characters.

    Parameters:
    - input_string (str): The string to sanitize.

    Returns:
    - str: The sanitized string.
    """
    # Step 1: Strip leading/trailing whitespace
    sanitized = input_string.strip()

    # Step 2: Remove unwanted characters (e.g., anything that's not
    # alphanumeric or common punctuation)
    sanitized = re.sub(
        r'[^a-zA-Z0-9 .,\'\"@#&()\-ÁáÂâÃãÀàÉéÊêÍíÓóÔôÕõÚúÇç]',
        '',
        sanitized
    )
    # Step 3: Replace sequences of whitespace (tabs, newlines)
    # with a single space
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Step 4: Escape HTML special characters to prevent XSS attacks
    sanitized = html.escape(sanitized)

    # Step 5: Put string into lowercase format
    sanitized = sanitized.lower()

    return sanitized
