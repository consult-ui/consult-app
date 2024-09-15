from typing import Optional

from pydantic import BaseModel


class OrganizationSuggestion(BaseModel):
    name: str
    tax_number: str
    head_name: Optional[str] = None


class ExternalOrganization(OrganizationSuggestion):
    address: Optional[str] = None
    activity_type: Optional[str] = None


class CreateOrganizationRequest(BaseModel):
    name: str
    activity_type: str
    tax_number: Optional[str] = None
    head_name: Optional[str] = None
    address: Optional[str] = None
    quarterly_income: Optional[int] = None
    quarterly_expenses: Optional[int] = None
    number_employees: Optional[int] = None
    average_receipt: Optional[int] = None
    context: Optional[str] = None


class PublicOrganization(BaseModel):
    id: int
    name: str
    activity_type: str
    tax_number: Optional[str] = None
    head_name: Optional[str] = None
    address: Optional[str] = None
    quarterly_income: Optional[int] = None
    quarterly_expenses: Optional[int] = None
    number_employees: Optional[int] = None
    average_receipt: Optional[int] = None
