from allure import step
from consult.pom.auth import access_token
from utils.api_client import client


@step("Создаем чат")
def create_chat(json=None):
    response = client.make_request(
        handle="/chat/create", method="POST", json=json, headers=access_token
    )
    return response


@step("Обновляем чат")
def update_chat_with_id(id, json=None):
    response = client.make_request(
        handle=f"/chat/{id}/update", method="PUT", json=json, headers=access_token
    )
    return response


@step("Удаляем чат")
def delete_chat_with_id(id):
    response = client.make_request(
        handle=f"/chat/{id}/delete", method="DELETE", headers=access_token
    )
    return response


@step("Получаем список чатов")
def get_list_of_chats():
    response = client.make_request(
        handle="/chat/list", method="GET", headers=access_token
    )
    return response


@step("Получаем список ассистентов")
def get_list_of_assistants():
    response = client.make_request(
        handle="/chat/assistant/list", method="GET", headers=access_token
    )
    return response
