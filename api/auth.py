from allure import step

from api.base_api import BaseApi
from data.users import USERS


class AuthApi(BaseApi):
    """
    Методы для аутентификации.
    """

    @step('Создать токен аутентификации')
    def create_token(self) -> dict:
        """
        Создание токена аутентификации.

        :return: результат выполнения запроса.
        """

        data = {
            'username': USERS['admin']['login'],
            'password': USERS['admin']['password'],
        }

        return self._post(url='auth', data=data)
