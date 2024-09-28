from http import HTTPStatus

from allure import title
from consult.pom.auth import login


@title("/auth/sign-in | POST")
def test_signin():
    response = login()
    response.status_code_should_be_eq(HTTPStatus.OK)
    response.value_with_key("msg").should_be_eq("ok")


def test_signin_with_wrong_credentials():
    response = login(json={"login": "admin", "password": "wrong"})
    response.status_code_should_be_eq(HTTPStatus.UNAUTHORIZED)
