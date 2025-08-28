from datetime import UTC, datetime, timedelta

import jwt

from config import jwt_settings


def create_access_token(data: dict):
    """
    Creates JWT-token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decodes JWT-token.
    """
    try:
        payload = jwt.decode(
            token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
