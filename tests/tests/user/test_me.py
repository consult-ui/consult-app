from allure import title
from consult.pom.user import get_me


@title("/user/me | GET")
def test_get_me():
    response = get_me()
    response.status_code_should_be_eq(200)
