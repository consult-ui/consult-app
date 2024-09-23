from consult.pom.user import get_me
from allure import title

@title("/user/me | GET")
def test_get_me(auth_token):
    response = get_me(auth_token)
    response.status_code_should_be_eq(200)



