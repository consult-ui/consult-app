from consult.pom.user import reset_password
from allure import title


@title("/user/reset-password | POST")
def test_reset_password(auth_token):
    response = reset_password(auth_token)
    response.status_code_should_be_eq(200)

# {
#   "success": true,
#   "msg": "ок",
#   "data": null,
#   "errors": null
# }
