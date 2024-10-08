from http import HTTPStatus

from consult.data.company import company_dict
from consult.pom.admin import delete_company
from consult.pom.company import create_company

from app.schemas.organization import CreateOrganizationRequest

# Чек лист
# 1. Создание организации
# 2. Мы не можем создать больше одной организации
# 3. Принимаются только корректные типы данных
# 4. Установлены ограничения на все поля
# 5. И так далее....


def test_create_company():
    delete_company()

    response = create_company(
        json=CreateOrganizationRequest(**company_dict).model_dump()
    )
    response.status_code_should_be_eq(HTTPStatus.OK)

    # Need to get response from pydantic model.
    response.json_should_contains(
        {
            "success": True,
            "msg": "ок",
            "data": {
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


def test_create_company_twice():
    delete_company()

    response = create_company(
        json=CreateOrganizationRequest(**company_dict).model_dump()
    )
    response.status_code_should_be_eq(HTTPStatus.OK)

    response = create_company(
        json=CreateOrganizationRequest(**company_dict).model_dump()
    )
    response.status_code_should_be_eq(HTTPStatus.BAD_REQUEST)
    response.json_should_be_eq(
        {
            "success": False,
            "msg": "организация уже создана",
            "data": None,
            "errors": None,
        }
    )
