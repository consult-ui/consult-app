from http import HTTPStatus

from consult.pom.company import search_company_with_tax_number


def test_search_company():
    response = search_company_with_tax_number(tax_number="7707083893")  # ИНН сбера.
    response.status_code_should_be_eq(HTTPStatus.OK)
    response.json_should_be_eq(
        {
            "success": True,
            "msg": "ок",
            "data": {
                "name": "ПАО СБЕРБАНК",
                "tax_number": "7707083893",
                "head_name": "Греф Герман Оскарович",
                "address": "г Москва, ул Вавилова, д 19",
                "activity_type": "Денежное посредничество прочее",
            },
            "errors": None,
        }
    )
