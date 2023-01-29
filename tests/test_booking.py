from datetime import date, timedelta
from random import choice, randint

from allure import epic, feature, title

from utils.generated_test_data import UserData
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

    @title('Успешное обновление бронирования')
    def test_update_booking_success(self, booking_api, create_booking):
        checkin = date.today() + timedelta(days=randint(0, 366))
        checkout = checkin + timedelta(days=randint(0, 366))
        booking = {
            'firstname': UserData().firstname(),
            'lastname': UserData().lastname(),
            'totalprice': randint(1, 100000),
            'depositpaid': choice([True, False]),
            'checkin': str(checkin),
            'checkout': str(checkout),
            'additionalneeds': choice(['Breakfast', 'Lunch', 'Dinner']),
        }

        booking_id = create_booking['bookingid']
        update_booking = booking_api.update_booking(
            booking_id=booking_id,
            firstname=booking['firstname'],
            lastname=booking['lastname'],
            total_price=booking['totalprice'],
            deposit_paid=booking['depositpaid'],
            checkin=booking['checkin'],
            checkout=booking['checkout'],
            additional_needs=booking['additionalneeds'],
        )

        json_schema_asserts(response=update_booking, name='update_booking')
        booking_api.should_be_updated_booking(
            booking_id=booking_id,
            expected_booking_info=booking,
        )
