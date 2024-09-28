from allure import step
from consult.data.company import company_dict
from consult.pom.auth import access_token
from utils.api_client import client

from app.schemas.organization import CreateOrganizationRequest


@step("Создаем организацию")
def create_company(json=CreateOrganizationRequest(**company_dict).model_dump()):
    response = client.make_request(
        handle="/organization/create", method="POST", json=json, headers=access_token
    )
    return response


@step("Получаем организацию по ИНН")
def search_company_with_tax_number(tax_number):
    response = client.make_request(
        handle=f"/organization/search?tax_number={tax_number}",
        method="GET",
        headers=access_token,
    )
    return response


@step("Получаем организацию по ID")
def get_company_with_id(id):
    response = client.make_request(
        handle=f"/organization/{id}", method="GET", headers=access_token
    )
    return response


@step("Предложение организации по ИНН")
def suggest_company(tax_number=None):
    response = client.make_request(
        handle=f"/organization/suggest?q={tax_number}",
        method="GET",
        headers=access_token,
    )
    return response
