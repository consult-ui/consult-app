from allure import step
from consult.data.signin import signin_dict
from utils.api_client import client


@step("Логинимся")
def login(json: dict = signin_dict):
    response = client.make_request(
        handle="/auth/sign-in",
        method="POST",
        json=json,
    )
    return response


@step("Получаем токен доступа")
def get_access_token(json=signin_dict):
    response = client.make_request(
        handle="/auth/sign-in", method="POST", json=json, attach=False
    )
    return {
        "Authorization": f"Bearer {response.response.json()['data']['access_token']}"
    }


access_token = get_access_token()


@step("Отправляем refresh токен")
def refresh_token(json=signin_dict):
    response = client.make_request(
        handle="/auth/refresh", method="POST", json=json, headers=access_token
    )
    return response


@step("Разлогиниваемся")
def logout():
    response = client.make_request(
        handle="/auth/sign-out", method="POST", headers=access_token
    )
    return response
