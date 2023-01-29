from json import JSONDecodeError

from allure import step
from requests import HTTPError, Response, Session

from utils.decorators import attach_curl_to_allure


class ResponseValidator:
    """
    Класс, проводящий первичную валидацию ответов API.
    """

    def __init__(self, client: 'BaseApi', success_codes: list[int] | None = None):
        self.client = client
        self.success_codes = success_codes

    def __enter__(self):
        self._previous_validator = self.client.validator
        self.client.validator = self

    def __exit__(self, *args):
        self.client.validator = self._previous_validator

    @staticmethod
    def get_error_reason(response: Response):
        """
        Получение тела ответа при ошибке.

        :param response: объект Response.
        """

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def validate_status_code(self, response: Response):
        """
        Валидация кода ответа.

        :param response: объект Response.
        """

        if self.success_codes:
            if response.status_code not in self.success_codes:
                reason = self.get_error_reason(response)
                raise AssertionError(
                    f'Сервер ответил с кодом {response.status_code} '
                    f'(ожидались {self.success_codes}):\n{reason}',
                )
        else:
            try:
                response.raise_for_status()
            except HTTPError:
                reason = self.get_error_reason(response)
                raise AssertionError(
                    f'Сервер ответил с кодом {response.status_code}:\n{reason}',
                )


class BaseApi:

    def __init__(self, base_url: str = 'https://restful-booker.herokuapp.com'):
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/100.0.4896.75 Safari/537.36',
            },
        )
        self.validator = ResponseValidator(client=self)

    def override_validation_rules(self, success_codes: list[int] | None = None):
        return ResponseValidator(self, success_codes)

    @attach_curl_to_allure()
    @step('Отправка запроса GET на URL-адрес - {url}')
    def _get(self, url: str, headers: dict | None = None, query: dict | None = None):
        """
        Отправка GET-запроса на сервер.

        :param url: url-адрес запроса.
        :param query: query-параметры запроса.
        :param headers: заголовки запроса.
        :return: ответ.
        """

        if headers is None:
            headers = {}

        response = self.session.get(
            url=f'{self.base_url}/{url}',
            verify=False,
            headers=headers,
            params=query,
        )
        self.validator.validate_status_code(response)

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    @attach_curl_to_allure()
    @step('Отправка запроса POST на URL-адрес - {url}')
    def _post(self, url: str, data: str | dict | None = None, headers: dict | None = None, query: dict | None = None,
              is_json: bool = True):
        """
        Отправка POST-запроса на сервер.

        :param url: url-адрес запроса.
        :param query: query-параметры запроса.
        :param headers: заголовки запроса.
        :param data: тело запроса.
        :param is_json: параметр, управляющий заголовком типа содержимого.
        :return: ответ.
        """

        if headers is None:
            headers = {}

        response = self.session.post(
            url=f'{self.base_url}/{url}',
            verify=False,
            data=None if is_json else data,
            json=data if is_json else None,
            headers=headers,
            params=query,
        )
        self.validator.validate_status_code(response)

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    @attach_curl_to_allure()
    @step('Отправка запроса PUT на URL-адрес - {url}')
    def _put(self, url: str, data: str | dict | None = None, headers: dict | None = None, auth: tuple | None = None,
             query: dict | None = None, cookies: dict | None = None, is_json: bool = True):
        """
        Отправка PUT-запроса на сервер.

        :param url: url-адрес запроса.
        :param query: query-параметры запроса.
        :param headers: заголовки запроса.
        :param data: тело запроса.
        :param cookies: куки.
        :param is_json: параметр, управляющий заголовком типа содержимого.
        :return: ответ.
        """

        if headers is None:
            headers = {}
        if auth is None:
            auth = ()
        if cookies is None:
            cookies = {}

        response = self.session.put(
            url=f'{self.base_url}/{url}',
            verify=False,
            data=None if is_json else data,
            json=data if is_json else None,
            headers=headers,
            auth=auth,
            params=query,
            cookies=cookies,
        )
        self.validator.validate_status_code(response)

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    @attach_curl_to_allure()
    @step('Отправка запроса PATCH на URL-адрес - {url}')
    def _patch(self, url: str, data: str | dict | None = None, headers: dict | None = None, auth: tuple | None = None,
               query: dict | None = None, cookies: dict | None = None, is_json: bool = True):
        """
        Отправка PUT-запроса на сервер.

        :param url: url-адрес запроса.
        :param query: query-параметры запроса.
        :param headers: заголовки запроса.
        :param data: тело запроса.
        :param is_json: параметр, управляющий заголовком типа содержимого.
        :return: ответ.
        """

        if headers is None:
            headers = {}
        if auth is None:
            auth = ()
        if cookies is None:
            cookies = {}

        response = self.session.patch(
            url=f'{self.base_url}/{url}',
            verify=False,
            data=None if is_json else data,
            json=data if is_json else None,
            headers=headers,
            auth=auth,
            params=query,
            cookies=cookies,
        )
        self.validator.validate_status_code(response)

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    @attach_curl_to_allure()
    @step('Отправка запроса DELETE на URL-адрес - {url}')
    def _delete(self, url: str, headers: dict | None = None, auth: tuple | None = None, query: dict | None = None,
                cookies: dict | None = None):
        """
        Отправка DELETE-запроса на сервер.

        :param url: url-адрес запроса.
        :param query: query-параметры запроса.
        :param headers: заголовки запроса.
        :return: ответ.
        """

        if headers is None:
            headers = {}
        if auth is None:
            auth = ()
        if cookies is None:
            cookies = {}

        response = self.session.delete(
            url=f'{self.base_url}/{url}',
            verify=False,
            headers=headers,
            auth=auth,
            params=query,
            cookies=cookies,
        )
        self.validator.validate_status_code(response)

        try:
            return response.json()
        except JSONDecodeError:
            return response.text
