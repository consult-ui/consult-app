from typing import Optional, Sequence, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import File


async def get_file_by_openai_id(
        db_session: AsyncSession,
        openai_id: str,
) -> Optional[File]:
    rs = await db_session.execute(
        select(File).where(File.openai_id == openai_id)
    )
    return rs.scalars().first()


async def get_files_by_openai_ids(
        db_session: AsyncSession,
        openai_ids: List[str],
) -> Sequence[File]:
    rs = await db_session.execute(
        select(File).where(File.openai_id.in_(openai_ids))
    )
    return rs.scalars().all()
