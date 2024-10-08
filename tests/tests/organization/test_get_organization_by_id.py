from curses.ascii import HT
from http import HTTPStatus

from consult.data.company import company_dict
from consult.pom.admin import delete_company
from consult.pom.company import create_company, get_company_with_id

from app.schemas.organization import CreateOrganizationRequest

# Чек лист
# 1. Существующий id
# 2. Несуществующий id
# 3. Невалидный тип данных


def test_get_organization_by_id():
    delete_company()
    company = create_company(
        json=CreateOrganizationRequest(**company_dict).model_dump()
    )

    company_id = company.response.json()["data"]["id"]

    response = get_company_with_id(company_id)
    response.status_code_should_be_eq(HTTPStatus.OK)
    response.json_should_be_eq(
        {
            "success": True,
            "msg": "ок",
            "data": {
                "id": company_id,
                "name": "string",
                "activity_type": "string",
                "tax_number": "string",
                "head_name": "string",
                "address": "string",
                "quarterly_income": 0,
                "quarterly_expenses": 0,
                "number_employees": 0,
                "average_receipt": 0,
            },
            "errors": None,
        }
    )


def test_get_organization_by_id_using_non_existent_id():
    delete_company()

    response = get_company_with_id(-1)
    response.status_code_should_be_eq(HTTPStatus.NOT_FOUND)
    response.json_should_be_eq(
        {
            "success": False,
            "msg": "организация не найдена",
            "data": None,
            "errors": None,
        }
    )
