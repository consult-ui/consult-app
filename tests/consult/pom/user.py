from utils.api_client import client
from allure import step

@step("Получаем информацию о пользователе")
def get_me(auth_token):
    response = client.make_request(
        handle="/user/me",
        method="GET",
        headers=auth_token,
    )
    return response

@step("Сбрасываем пароль")
def reset_password(auth_token, json={"email": "johnmakarovqa@gmail.com"}):
    response = client.make_request(
        handle="/user/reset-password",
        method="POST",
        json=json,
        headers=auth_token
    )
    return response


