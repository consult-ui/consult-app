from typing import Sequence, List

from app.models.assistant import Assistant
from app.schemas.assistant import PublicAssistant


def make_public_assistants(assistants: Sequence[Assistant]) -> List[PublicAssistant]:
    dtos = []
    for assistant in assistants:
        a = PublicAssistant(
            id=assistant.id,
            name=assistant.name,
            desc=assistant.desc,
            color=assistant.color,
            icon_url=assistant.icon_url,
        )
        dtos.append(a)
    return dtos
