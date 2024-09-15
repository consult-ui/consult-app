from pydantic import BaseModel


class OrganizationSuggestion(BaseModel):
    tax_number: str
    name: str
