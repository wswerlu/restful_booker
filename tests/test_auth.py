from allure import epic, feature, title
from pytest import mark

from utils.helpers import get_booking_data, json_schema_asserts


@epic('Api')
@feature('Аутентификация')
@mark.not_parallel
class TestAuth:
    """
    Тесты для проверки аутентификации
    """

    @title('Успешное создание токена аутентификации')
    def test_create_token_success(self, auth_api):
        create_token = auth_api.create_token()
        json_schema_asserts(response=create_token, name='create_token')

    @title('Аутентификация в методе PUT /booking/:id с валидными данными')
    def test_update_booking_method_with_valid_auth_data(self, booking_api, create_booking, create_token,
                                                        data_auth_validauth):
        booking_data = get_booking_data()

        booking_api.update_booking(
            booking_id=create_booking['bookingid'],
            firstname=booking_data['firstname'],
            lastname=booking_data['lastname'],
            total_price=booking_data['totalprice'],
            deposit_paid=booking_data['depositpaid'],
            checkin=booking_data['checkin'],
            checkout=booking_data['checkout'],
            additional_needs=booking_data['additionalneeds'],
            token=create_token['token'] if data_auth_validauth[0] else None,
        )

    @title('Удаление бронирования с невалидными данными аутентификации')
    def test_delete_booking_with_invalid_auth_data(self, booking_api, create_booking, data_auth_invalidauth):
        booking_id = create_booking['bookingid']

        with booking_api.override_validation_rules(success_codes=[403]):
            booking_api.delete_booking(
                booking_id=booking_id,
                token=data_auth_invalidauth[0] if data_auth_invalidauth[0] else None,
                bauth_login=data_auth_invalidauth[1] if data_auth_invalidauth[1] else None,
                bauth_pass=data_auth_invalidauth[2] if data_auth_invalidauth[2] else None,
            )
