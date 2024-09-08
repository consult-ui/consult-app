import contextlib
from typing import Any, AsyncIterator

from app.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from app.schemas.base import json_serializer

Base = declarative_base()

# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


class DatabaseSessionManager:
    def __init__(self, dsn: str, engine_kwargs=None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(dsn, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine,
        )

    def has_engine(self) -> bool:
        return self._engine is not None

    @property
    def engine(self) -> Any:
        return self._engine

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    settings.pg_dsn,
    {
        "echo": settings.pg_echo,
        "json_serializer": json_serializer,
        "pool_size": 15,
        "max_overflow": 5,
    },
)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
