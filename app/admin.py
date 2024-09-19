import base64
from datetime import datetime, UTC

import jwt
from loguru import logger
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from wtforms import fields
from wtforms.validators import DataRequired

from app.config import settings
from app.models.assistant import Assistant
from app.models.chat import Chat
from app.models.message import Message
from app.models.organization import Organization
from app.models.refresh_session import RefreshSession
from app.models.user import User
from app.utils.auth import JWT_ALGORITHM, JWT_EXPIRATION_DELTA, ph


class AssistantAdmin(ModelView, model=Assistant):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-robot"

    column_list = "__all__"
    column_searchable_list = [Assistant.name, Assistant.desc, Assistant.instruction]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    form_excluded_columns = [Assistant.id, Assistant.created_at, Assistant.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]


class MessageAdmin(ModelView, model=Message):
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-comment"

    column_searchable_list = [Message.chat_id]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [Message.created_at]

    form_excluded_columns = [Message.id, Message.created_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]


class ChatAdmin(ModelView, model=Chat):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-headset"

    column_searchable_list = [Chat.name, Chat.desc, Chat.system_prompt]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [Chat.updated_at]

    form_excluded_columns = [Chat.id, Chat.created_at, Chat.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]


class OrganizationAdmin(ModelView, model=Organization):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-briefcase"

    column_searchable_list = [Organization.name, Organization.tax_number, Organization.head_name]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [Organization.updated_at]

    form_excluded_columns = [Organization.id, Organization.created_at, Organization.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]


class PasswordField(fields.PasswordField):
    def _value(self):
        if self.data:
            return ph.hash(self.data)
        return ""

    def process_formdata(self, valuelist):
        if not valuelist:
            raise ValueError("Invalid password")
        try:
            self.data = ph.hash(valuelist[0])
        except ValueError:
            raise ValueError("Invalid password")


class RefreshSessionAdmin(ModelView, model=RefreshSession):
    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-key"

    column_list = "__all__"

    column_searchable_list = ["user_id", "refresh_token"]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    page_size = 25
    page_size_options = [25, 50, 100, 200]


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

    column_exclude_list = [User.password, User.updated_at]

    page_size = 25
    page_size_options = [25, 50, 100, 200]

    form_columns = [
        User.phone_number,
        User.email,
        User.password,
        User.first_name,
        User.last_name,
        User.expiration_date,
        User.whatsapp_url,
        User.telegram_url,
    ]

    form_overrides = dict(password=PasswordField)

    form_args = dict(
        password=dict(
            label="Password",
            validators=[DataRequired()],
        )
    )


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
