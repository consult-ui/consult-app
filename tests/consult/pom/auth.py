from utils.api_client import client
from consult.data.signin import signin_dict
from allure import step


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
        handle="/auth/sign-in",
        method="POST",
        json=json
    )
    return {"Authorization": f"Bearer {response.response.json()['data']['access_token']}"}