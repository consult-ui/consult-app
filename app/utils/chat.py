from typing import Sequence, List

from app.schemas.chat import PublicChat


def make_public_chats(chats: Sequence) -> List[PublicChat]:
    dtos = []
    for chat in chats:
        p = PublicChat(
            id=chat.id,
            name=chat.name,
            desc=chat.desc,
            color=chat.color,
            icon_url=chat.icon_url,
            created_at=chat.created_at,
        )
        dtos.append(p)
    return dtos
