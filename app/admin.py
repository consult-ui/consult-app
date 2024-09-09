import base64
from datetime import datetime, timedelta, UTC

import argon2
import jwt
from loguru import logger
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.config import settings
from app.models.user import User


class UserAdmin(ModelView, model=User):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-user"

    column_searchable_list = ["phone_number", "email", "first_name", "last_name"]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [User.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]

    form_columns = [
        User.phone_number,
        User.email,
        User.first_name,
        User.last_name,
        User.expiration_date,
    ]

    async def on_model_change(self, data, model: User, is_created, request):
        if is_created:
            model.password = ph.hash(data["password"])


JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(hours=48)

ph = argon2.PasswordHasher()


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
