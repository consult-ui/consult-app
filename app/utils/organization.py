from app.models.organization import Organization
from app.schemas.organization import PublicOrganization


def make_public_organization(org: Organization) -> PublicOrganization:
    return PublicOrganization(
        id=org.id,
        name=org.name,
        activity_type=org.activity_type,
        tax_number=org.tax_number,
        head_name=org.head_name,
        address=org.address,
        quarterly_income=org.quarterly_income,
        quarterly_expenses=org.quarterly_expenses,
        number_employees=org.number_employees,
        average_receipt=org.average_receipt,
    )
