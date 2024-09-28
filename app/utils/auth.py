import base64
from datetime import datetime, UTC
from datetime import timezone, timedelta

import argon2
import jwt
from loguru import logger
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

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


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        hs = base64.b64decode(settings.admin_password_hash).decode("utf-8")

        logger.debug(f"hash {hs}")

        try:
            if not ph.verify(hs, str(password)):
                return False
        except Exception as e:
            logger.error(e)
            return False

        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.now(UTC) + JWT_EXPIRATION_DELTA,
            },
            settings.jwt_secret,
            algorithm=JWT_ALGORITHM,
        )

        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[JWT_ALGORITHM])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
