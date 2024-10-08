from allure import step
from consult.config import settings
from consult.pom.user import get_me
from utils.api_client import client


@step("Удаляем организацию")
def delete_company(
    data: str = f"username={settings.admin_login}&password={settings.admin_password}",
):

    login = client.make_request(
        handle="/admin/login",
        method="POST",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    company_id = get_me().response.json()["data"]["organization_id"]

    login_cookies = login.response.cookies

    client.make_request(
        handle=f"/admin/organization/delete?pks={company_id}",
        method="DELETE",
        cookies=login_cookies,
    )
