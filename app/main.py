import sys
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqladmin import Admin

import app.routers.auth as auth
import app.routers.chat as chat
import app.routers.contact as contact
import app.routers.organization as organization
import app.routers.user as user
from app.admins.assistant import AssistantAdmin
from app.admins.chat import ChatAdmin
from app.admins.contact_request import ContactRequestAdmin
from app.admins.file import FileAdmin
from app.admins.message import MessageAdmin
from app.admins.organization import OrganizationAdmin
from app.admins.refresh_session import RefreshSessionAdmin
from app.admins.user import UserAdmin
from app.config import settings, STATIC_FOLDER
from app.exceptions import register_exception_handlers
from app.utils.auth import AdminAuth
from app.utils.db import sessionmanager

uvloop.install()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.remove()
    logger.add(sys.stderr, level=settings.log_lvl)

    logger.info("🚀 Starting application")

    yield

    logger.info("⛔ Stopping application")

    if sessionmanager.has_engine():
        await sessionmanager.close()


logger.info(f"📚 Docs are {'enabled' if settings.show_docs == 'true' else 'disabled'}")

app = FastAPI(  # noqa
    root_path="/api/v1",
    lifespan=lifespan,
    docs_url="/docs" if settings.show_docs else None,
    redoc_url="/redoc" if settings.show_docs else None,
    openapi_url="/openapi.json" if settings.show_docs else None,
)


@app.get("/ping")
async def ping():
    return "ok!"


app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(chat.router)
app.include_router(contact.router)

admin = Admin(
    app=app,
    engine=sessionmanager.engine,
    authentication_backend=AdminAuth(secret_key=settings.jwt_secret),
    templates_dir=STATIC_FOLDER + "/templates",
)

admin.add_view(UserAdmin)
admin.add_view(RefreshSessionAdmin)
admin.add_view(OrganizationAdmin)
admin.add_view(ChatAdmin)
admin.add_view(MessageAdmin)
admin.add_view(AssistantAdmin)
admin.add_view(ContactRequestAdmin)
admin.add_view(FileAdmin)
