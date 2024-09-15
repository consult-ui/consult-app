from typing import Optional

from pydantic import BaseModel


class OrganizationSuggestion(BaseModel):
    tax_number: str
    name: str
    head_name: Optional[str] = None
