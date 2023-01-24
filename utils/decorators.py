from json import dumps
from typing import Callable

from allure_commons._allure import attach
from allure_commons.types import AttachmentType
from curlify import to_curl
from requests.models import Response


def attach_curl_to_allure():
    """
    Декоратор для генерации cURL и сохранения запроса и ответа в отчёт Allure.
    """

    def wrapper(func: Callable[..., Response]):
        def main(*args, **kwargs):
            response = func(*args, **kwargs)
            try:
                attach(
                    body=to_curl(response.request),
                    attachment_type=AttachmentType.TEXT,
                    name='request',
                )
            except Exception as e:
                print(e)
            try:
                content = response.text
                header_value = response.headers.get('Content-Type', '')
                if header_value.startswith('text/html'):
                    content_type = AttachmentType.HTML
                elif header_value.startswith('application/json'):
                    content_type = AttachmentType.JSON
                    content = dumps(response.json(), ensure_ascii=False, indent=4)
                else:
                    content_type = AttachmentType.TEXT

                attach(
                    body=content,
                    attachment_type=content_type,
                    name='response',
                )
            except Exception as e:
                print(e)
            return response

        return main

    return wrapper
