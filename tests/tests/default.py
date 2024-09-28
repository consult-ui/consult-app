from http import HTTPStatus

from allure import title
from utils.api_client import client

title("/ping | GET")


def test_default():
    response = client.make_request(
        handle="/ping",
        method="GET",
    )
    response.status_code_should_be_eq(HTTPStatus.OK)
    response.json_should_be_eq("ok!")
