from allure import epic, feature, title

from utils.helpers import get_booking_data, json_schema_asserts


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

    @title('Обновление бронирования с использованием токена аутентификации')
    def test_update_booking_with_auth_token(self, booking_api, create_booking, create_token):
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
            token=create_token['token'],
        )

    @title('Удаление бронирования с невалидным токеном')
    def test_delete_booking_with_invalid_auth_token(self, booking_api, create_booking):
        booking_id = create_booking['bookingid']

        with booking_api.override_validation_rules(success_codes=[403]):
            booking_api.delete_booking(booking_id=booking_id, token='invalid_token')
