from allure import epic, feature, title

from utils.helpers import json_schema_asserts


@epic('Api')
@feature('Аутентификация')
class TestBooking:
    """
    Тесты для проверки аутентификации
    """

    @title('Успешное создание токена аутентификации')
    def test_create_token_success(self, auth_api):
        create_token = auth_api.create_token()
        json_schema_asserts(response=create_token, name='create_token')
