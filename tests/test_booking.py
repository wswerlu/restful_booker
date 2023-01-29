from random import randint

from allure import epic, feature, title

from utils.helpers import get_updated_date, json_schema_asserts


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
        booking_id = create_booking['bookingid']
        booking_data = {
            'firstname': create_booking['booking']['firstname'] + 'test',
            'lastname': create_booking['booking']['lastname'] + 'test',
            'totalprice': create_booking['booking']['totalprice'] + randint(1, 100),
            'depositpaid': not create_booking['booking']['depositpaid'],
            'checkin': get_updated_date(old_date=create_booking['booking']['bookingdates']['checkin']),
            'checkout': get_updated_date(old_date=create_booking['booking']['bookingdates']['checkout']),
            'additionalneeds': create_booking['booking']['additionalneeds'] + 'test',
        }

        update_booking = booking_api.update_booking(
            booking_id=booking_id,
            firstname=booking_data['firstname'],
            lastname=booking_data['lastname'],
            total_price=booking_data['totalprice'],
            deposit_paid=booking_data['depositpaid'],
            checkin=booking_data['checkin'],
            checkout=booking_data['checkout'],
            additional_needs=booking_data['additionalneeds'],
        )
        json_schema_asserts(response=update_booking, name='update_booking')

        booking_api.should_be_updated_booking(
            booking_id=booking_id,
            expected_booking_info=booking_data,
        )
