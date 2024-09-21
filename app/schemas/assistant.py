from pydantic import BaseModel


class PublicAssistant(BaseModel):
    id: int
    name: str
    desc: str
    color: str
    icon_url: str
