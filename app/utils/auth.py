import argon2
import jwt

from datetime import timezone, datetime, timedelta
from app.config import settings

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(hours=48)

ph = argon2.PasswordHasher()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=JWT_ALGORITHM)
    return encoded_jwt
