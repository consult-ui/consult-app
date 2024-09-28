import json

import allure
import requests
from allure_commons.types import AttachmentType
from consult.config import settings
from curlify2 import Curlify
from loguru import logger
from requests import Response
from utils.api_response import APIResponse


class APIClient:
    # TODO: add another class for logging.
    @staticmethod
    def response_logging(response: Response):
        logger.info("Запрос на ручку: " + str(response.request.url))
        if response.request.body:
            if isinstance(response.request.body, bytes):
                logger.debug("Тело запроса: " + response.request.body.decode("utf-8"))
            else:
                logger.debug("Тело запроса: " + response.request.body)
        logger.debug("Заголовки запроса: " + str(response.request.headers))
        logger.info("Код ответа: " + str(response.status_code))
        logger.debug("Тело ответа: " + response.text)
        logger.debug("Curl: " + Curlify(response.request, compressed=True).to_curl())

    @staticmethod
    def send_request(response: Response):

        if response.request.headers:
            allure.attach(
                body=str(response.request.headers),
                name="Заголовки запроса",
                attachment_type=AttachmentType.TEXT,
            )

        if response.request.body:
            content_str = response.request.body.decode("utf-8")
            json_content = json.dumps(
                json.loads(content_str), indent=4, ensure_ascii=False
            )
            allure.attach(
                body=json_content,
                name="Тело запроса",
                attachment_type=AttachmentType.JSON,
                extension="json",
            )

    @staticmethod
    def get_response(response: Response):
        allure.attach(
            body=str(response.status_code),
            name="Код ответа",
            attachment_type=AttachmentType.TEXT,
        )

        if response.text:
            try:
                json_response = response.json()
                allure.attach(
                    body=json.dumps(json_response, indent=4, ensure_ascii=False),
                    name="Тело ответа",
                    attachment_type=AttachmentType.JSON,
                    extension="json",
                )
            except ValueError:
                allure.attach(
                    body=response.text,
                    name="Тело ответа",
                    attachment_type=AttachmentType.TEXT,
                )

    @staticmethod
    def useful_info(response: Response):
        allure.attach(
            body=Curlify(response.request, compressed=True).to_curl(),
            name="Curl запроса",
            attachment_type=AttachmentType.TEXT,
        )

    # TODO: add auto authorization
    def make_request(
        self,
        handle: str,
        method: str,
        json=None,
        data=None,
        params=None,
        headers=None,
        attach=True,
        cookies=None,
    ):
        response = requests.request(
            method,
            url=settings.base_url + handle,
            json=json,
            data=data,
            params=params,
            headers=headers,
            cookies=cookies,
        )

        self.response_logging(response)

        if attach:
            with allure.step(
                f"Отправляем {response.request.method} запрос на ручку: {response.request.url}"
            ):
                self.send_request(response)
                self.get_response(response)
                self.useful_info(response)

        return APIResponse(response)


client = APIClient()
