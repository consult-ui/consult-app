from typing import Optional

from pydantic import BaseModel


class OrganizationSuggestion(BaseModel):
    name: str
    tax_number: str
    head_name: Optional[str] = None


class ExternalOrganization(OrganizationSuggestion):
    address: Optional[str] = None
    activity_type: Optional[str] = None
