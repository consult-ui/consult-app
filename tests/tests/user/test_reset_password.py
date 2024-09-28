from allure import title
from consult.pom.user import reset_password


@title("/user/reset-password | POST")
def test_reset_password():
    response = reset_password()
    response.status_code_should_be_eq(200)
    response.json_should_be_eq(
        {"success": True, "msg": "ок", "data": None, "errors": None}
    )
