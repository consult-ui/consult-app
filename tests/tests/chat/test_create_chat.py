from http import HTTPStatus

from consult.pom.admin import delete_company
from consult.pom.chat import create_chat
from consult.pom.company import create_company


def test_create_chat():
    delete_company()

    # TODO: add function for path getting from response.

    create_company()
    chat = create_chat({"assistant_id": 1})
    chat.status_code_should_be_eq(HTTPStatus.OK)
    chat.json_should_contains(
        {
            "success": True,
            "msg": "чат создан",
            "data": {
                # "id": 1, # TODO: need to get id for checking.
                "name": "Юрист",
                "desc": "Чат для юридический вопросов",
                "color": "#34a1eb",
                "icon_url": "https://chat-preview.lobehub.com/icons/icon-192x192.png",
                # "created_at": "2024-09-28T13:24:47.024641Z", # TODO: need to get time for checking.
            },
            "errors": None,
        }
    )
    # chat.schema_should_be_eq()
