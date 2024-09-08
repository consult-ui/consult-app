import asyncio
import sys
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqladmin import Admin

import app.bot.message_handlers.handlers  # noqa
import app.routers.bot as bot
import app.routers.case as case
import app.routers.case_inventory_withdraw as case_inventory_withdraw
import app.routers.crash as crash
import app.routers.daily as daily
import app.routers.farm as farm
import app.routers.game as game
import app.routers.inventory as inventory
import app.routers.invite as invite
import app.routers.multiplier as multiplier
import app.routers.profile as profile
import app.routers.raffle as raffle
import app.routers.rain as rain
import app.routers.s2s as s2s
import app.routers.steam as steam
import app.routers.task as task
import app.routers.user as user
from app.background import (
    create_raffle_task,
    sending_messages_to_users,
    send_farm_notifications_task,
    send_sparks_notifications_task,
    send_daily_claim_notifications_task,
    process_new_withdrawals,
    process_trade_status_transitions,
)
from app.bot.bot import run_bot
from app.config import settings, STATIC_FOLDER
from app.db import sessionmanager
from app.exceptions import register_exception_handlers
from app.admin import (
    UserAdmin,
    Levels,
    TaskAdmin,
    AdminAuth,
    ProjectAdmin,
    UserTaskAdmin,
    MultiplierAdmin,
    AppSettingsAdmin,
    RainSettingsAdmin,
    StreakRewardsAdmin,
    CaseAdmin,
    LiderboardView,
    CrashRoundAdmin,
    RainManagement,
    RainEventAdmin,
    RaffleAdmin,
    NotificationManagement,
    WithdrawalAdmin,
    WithdrawableAssetAdmin,
    APIKeyAdmin,
)

uvloop.install()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.remove()
    logger.add(sys.stderr, level=settings.log_lvl)

    logger.info("🚀 Starting application")

    async with sessionmanager.session() as session1:
        await run_bot(session1)

    asyncio.create_task(create_raffle_task())

    asyncio.create_task(sending_messages_to_users())
    asyncio.create_task(send_farm_notifications_task())
    asyncio.create_task(send_daily_claim_notifications_task())
    asyncio.create_task(send_sparks_notifications_task())
    asyncio.create_task(process_new_withdrawals())
    asyncio.create_task(process_trade_status_transitions())

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
