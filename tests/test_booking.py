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

    @title('Успешное частичное обновление бронирования')
    def test_partial_update_booking_success(self, booking_api, create_booking, data_booking_partialupdate):
        booking_id = create_booking['bookingid']
        booking_data = {
            'firstname': create_booking['booking']['firstname'] + 'test'
            if data_booking_partialupdate[0] else create_booking['booking']['firstname'],
            'lastname': create_booking['booking']['lastname'] + 'test'
            if data_booking_partialupdate[1] else create_booking['booking']['lastname'],
            'totalprice': create_booking['booking']['totalprice'] + randint(1, 100)
            if data_booking_partialupdate[2] else create_booking['booking']['totalprice'],
            'depositpaid': not create_booking['booking']['depositpaid']
            if data_booking_partialupdate[3] else create_booking['booking']['depositpaid'],
            'checkin': get_updated_date(old_date=create_booking['booking']['bookingdates']['checkin'])
            if data_booking_partialupdate[4] else create_booking['booking']['bookingdates']['checkin'],
            'checkout': get_updated_date(old_date=create_booking['booking']['bookingdates']['checkout'])
            if data_booking_partialupdate[5] else create_booking['booking']['bookingdates']['checkout'],
            'additionalneeds': create_booking['booking']['additionalneeds'] + 'test'
            if data_booking_partialupdate[6] else create_booking['booking']['additionalneeds'],
        }

        partial_update_booking = booking_api.partial_update_booking(
            booking_id=booking_id,
            firstname=booking_data['firstname'] if data_booking_partialupdate[0] else None,
            lastname=booking_data['lastname'] if data_booking_partialupdate[1] else None,
            total_price=booking_data['totalprice'] if data_booking_partialupdate[2] else None,
            deposit_paid=booking_data['depositpaid'] if data_booking_partialupdate[3] else None,
            checkin=booking_data['checkin'] if data_booking_partialupdate[4] or data_booking_partialupdate[5] else None,
            checkout=booking_data['checkout']
            if data_booking_partialupdate[4] or data_booking_partialupdate[5] else None,
            additional_needs=booking_data['additionalneeds'] if data_booking_partialupdate[6] else None,
        )
        json_schema_asserts(response=partial_update_booking, name='update_booking')

        booking_api.should_be_updated_booking(
            booking_id=booking_id,
            expected_booking_info=booking_data,
        )

    @title('Успешное удаление бронирования')
    def test_delete_booking_success(self, booking_api, create_booking):
        booking_id = create_booking['bookingid']

        booking_api.delete_booking(booking_id=booking_id)

        booking_api.should_not_be_booking_with_id(
            booking_id=booking_id,
            firstname=create_booking['booking']['firstname'],
            lastname=create_booking['booking']['lastname'],
        )

    @title('Успешное получение информации по бронированию')
    def test_get_booking_success(self, booking_api, create_booking):
        booking_id = create_booking['bookingid']

        booking = booking_api.get_booking_info(booking_id=booking_id)
        json_schema_asserts(response=booking, name='get_booking')

    @title('Успешное получение id бронирований')
    def test_get_booking_ids_success(self, booking_api, create_booking, data_booking_bookingids):
        booking_id = booking_api.get_bookings_ids(
            firstname=create_booking['booking']['firstname'] if data_booking_bookingids[0] else None,
            lastname=create_booking['booking']['lastname'] if data_booking_bookingids[1] else None,
            checkin=create_booking['booking']['bookingdates']['checkin'] if data_booking_bookingids[2] else None,
            checkout=create_booking['booking']['bookingdates']['checkout'] if data_booking_bookingids[3] else None,
        )
        json_schema_asserts(response=booking_id, name='get_booking_ids')

    @title('Получение информации по бронированию с несуществующим id')
    def test_get_booking_with_non_existent_booking_id(self, booking_api):
        non_existent_booking_id = booking_api.get_max_booking_id() + 1000

        with booking_api.override_validation_rules(success_codes=[404]):
            booking_api.get_booking_info(booking_id=non_existent_booking_id)

    @title('Создание бронирования без обязательных параметров')
    def test_create_booking_without_required_parameters(self, booking_api, data_booking_requiredparameters):
        with booking_api.override_validation_rules(success_codes=[500]):
            booking_api.create_booking(
                firstname=data_booking_requiredparameters[0] if data_booking_requiredparameters[0] else None,
                lastname=data_booking_requiredparameters[1] if data_booking_requiredparameters[1] else None,
                total_price=data_booking_requiredparameters[2] if data_booking_requiredparameters[2] else None,
                deposit_paid=data_booking_requiredparameters[3] if data_booking_requiredparameters[3] else None,
                checkin=data_booking_requiredparameters[4] if data_booking_requiredparameters[4] else None,
                checkout=data_booking_requiredparameters[5] if data_booking_requiredparameters[5] else None,
                is_random=False,
            )
