import sys
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqladmin import Admin

from app.config import settings, STATIC_FOLDER
from app.db import sessionmanager
from app.exceptions import register_exception_handlers
from app.admin import AdminAuth, UserAdmin


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
    docs_url="/docs" if settings.show_docs == "true" else None,
    redoc_url="/redoc" if settings.show_docs == "true" else None,
    openapi_url="/openapi.json" if settings.show_docs == "true" else None,
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

# app.include_router(user.router)

admin = Admin(
    app=app,
    engine=sessionmanager.engine,
    authentication_backend=AdminAuth(secret_key=settings.jwt_secret),
    templates_dir=STATIC_FOLDER + "/templates",
)

admin.add_view(UserAdmin)
