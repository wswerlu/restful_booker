from allure import epic, feature, title

from utils.helpers import json_schema_asserts


@epic('Api')
@feature('Бронирование')
class TestBooking:
    """
    Тесты для проверки бронирования
    """

    @title('Успешное создание бронирования')
    def test_create_booking_success(self, booking_api):
        booking = booking_api.create_booking()
        json_schema_asserts(response=booking, name='create_booking')
        booking_id = booking['bookingid']
        booking_api.should_be_booking_with_id(
            booking_id=booking_id,
            firstname=booking['booking']['firstname'],
            lastname=booking['booking']['lastname'],
        )
