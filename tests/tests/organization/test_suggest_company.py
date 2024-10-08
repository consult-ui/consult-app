from http import HTTPStatus

from consult.pom.company import suggest_company


def test_suggest_company():
    response = suggest_company(tax_number="7707083893")
    response.status_code_should_be_eq(HTTPStatus.OK)
