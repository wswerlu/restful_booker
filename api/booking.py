from datetime import date, timedelta
from random import choice, randint

from allure import step

from api.base_api import BaseApi
from data.users import USERS
from utils.generated_test_data import UserData


class BookingApi(BaseApi):
    """
    Методы для работы с бронированием.
    """

    @step('Создать бронирование')
    def create_booking(self, firstname: str | None = None, lastname: str | None = None, total_price: int | None = None,
                       deposit_paid: bool | None = None, checkin: str | None = None, checkout: str | None = None,
                       additional_needs: str | None = None, is_random: bool = True) -> dict:
        """
        Создание бронирования.

        :param firstname: имя.
        :param lastname: фамилия.
        :param total_price: стоимость бронирования.
        :param deposit_paid: True — депозит внесен, False — депозит не внесен.
        :param checkin: дата заезда.
        :param checkout: дата отъезда.
        :param additional_needs: дополнительные пожелания по бронированию.
        :param is_random: True — бронирование с произвольными данными (остальные параметры указывать не надо),
         False — бронирование с конкретными данными.
        :return: результат выполнения запроса.
        """

        if is_random:
            user = UserData()
            firstname = user.firstname()
            lastname = user.lastname()
            total_price = randint(1, 100000)
            deposit_paid = choice([True, False])
            checkin = date.today() + timedelta(days=randint(0, 366))
            checkout = checkin + timedelta(days=randint(0, 366))
            additional_needs = choice(['Breakfast', 'Lunch', 'Dinner'])

        data = {
            'firstname': firstname,
            'lastname': lastname,
            'totalprice': total_price,
            'depositpaid': deposit_paid,
            'bookingdates': {
                'checkin': str(checkin),
                'checkout': str(checkout),
            },
            'additionalneeds': additional_needs,
        }

        return self._post(url='booking', data=data)

    @step('Получить список с id бронирований')
    def get_bookings_ids(self, firstname: str | None = None, lastname: str | None = None, checkin: str | None = None,
                         checkout: str | None = None) -> list:
        """
        Получение списка с id бронирований.

        :param firstname: имя.
        :param lastname: фамилия.
        :param checkin: дата заезда.
        :param checkout: дата отъезда.
        :return: результат выполнения запроса.
        """

        query = {
            'firstname': firstname,
            'lastname': lastname,
            'checkin': checkin,
            'checkout': checkout,
        }

        return self._get(url='booking', query=query)

    @step('Проверить, что существует бронирование с id: {booking_id}')
    def should_be_booking_with_id(self, booking_id: int, firstname: str | None = None, lastname: str | None = None,
                                  checkin: str | None = None, checkout: str | None = None) -> None:
        """
        Проверка существования бронирования с указанным id.

        :param booking_id: id бронирования.
        :param firstname: имя.
        :param lastname: фамилия.
        :param checkin: дата заезда.
        :param checkout: дата отъезда.
        """

        response = self.get_bookings_ids(firstname=firstname, lastname=lastname, checkin=checkin, checkout=checkout)
        bookings_ids = [x['bookingid'] for x in response]

        assert booking_id in bookings_ids, f'Не существует бронирования с id: {booking_id}'

    @step('Обновить бронирование с id {booking_id}')
    def update_booking(self, booking_id: int, firstname: str, lastname: str, total_price: int, deposit_paid: bool,
                       checkin: str, checkout: str, additional_needs: str) -> dict:
        """
        Обновление указанного бронирования.

        :param booking_id: id бронирования.
        :param firstname: имя.
        :param lastname: фамилия.
        :param total_price: стоимость бронирования.
        :param deposit_paid: True — депозит внесен, False — депозит не внесен.
        :param checkin: дата заезда.
        :param checkout: дата отъезда.
        :param additional_needs: дополнительные пожелания по бронированию.
        :return: результат выполнения запроса.
        """

        auth = (USERS['admin']['login'], USERS['admin']['password'])

        data = {
            'firstname': firstname,
            'lastname': lastname,
            'totalprice': total_price,
            'depositpaid': deposit_paid,
            'bookingdates': {
                'checkin': str(checkin),
                'checkout': str(checkout),
            },
            'additionalneeds': additional_needs,
        }

        return self._put(url=f'booking/{booking_id}', data=data, auth=auth)

    @step('Получить информацию по бронированию с id: {booking_id}')
    def get_booking_info(self, booking_id: int) -> dict:
        """
        Получение списка с id бронирований.

        :param booking_id: id бронирования.
        :return: результат выполнения запроса.
        """

        return self._get(url=f'booking/{booking_id}')

    @step('Проверить, что бронирование с id: {booking_id} обновлено')
    def should_be_updated_booking(self, booking_id: int, expected_booking_info: dict) -> None:
        """
        Проверка существования бронирования с указанным id.

        :param booking_id: id бронирования.
        :param expected_booking_info: словарь с данными, которые должны быть в бронировании после обновления.
        """

        actual_booking_info = self.get_booking_info(booking_id=booking_id)

        for key in expected_booking_info.keys():
            expected_data = expected_booking_info[key]

            if key in ['checkin', 'checkout']:
                actual_data = actual_booking_info['bookingdates'][key]
            else:
                actual_data = actual_booking_info[key]

            assert actual_data == expected_data, \
                f'Текущее значение ключа {key!r}: {actual_data} не соответствует ожидаемому: {expected_data}'
