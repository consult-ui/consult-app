from consult.pom.auth import login
from http import HTTPStatus
from allure import title

@title("/auth/sign-in | POST")
def test_signin():
    response = login()
    response.status_code_should_be_eq(HTTPStatus.OK)
    response.value_with_key("msg").should_be_eq("ok")

    
