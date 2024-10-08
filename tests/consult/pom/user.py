from allure import step
from consult.config import settings
from consult.pom.auth import access_token
from utils.api_client import client


@step("Получаем информацию о пользователе")
def get_me():
    response = client.make_request(
        handle="/user/me",
        method="GET",
        headers=access_token,
    )
    return response


@step("Отправляем заявку на восстановление пароля")
def reset_password(json={"email": settings.email_for_testing}):
    response = client.make_request(
        handle="/user/reset-password", method="POST", json=json, headers=access_token
    )
    return response
