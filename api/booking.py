from datetime import date, timedelta
from random import choice, randint

from allure import step

from api.base_api import BaseApi
from utils.generated_test_data import UserData


class BookingApi(BaseApi):
    """
    Методы для работы с бронью.
    """

    @step('Создать бронь')
    def create_booking(self, firstname: str | None = None, lastname: str | None = None, total_price: int | None = None,
                       deposit_paid: bool | None = None, checkin: str | None = None, checkout: str | None = None,
                       additional_needs: str = 'Breakfast', is_random: bool = True) -> dict:
        """
        Создание брони.

        :param firstname: имя.
        :param lastname: фамилия.
        :param total_price: стоимость брони.
        :param deposit_paid: True — депозит внесен, False — депозит не внесен.
        :param checkin: дата заезда.
        :param checkout: дата отъезда.
        :param additional_needs: дополнительные пожелания по брони.
        :param is_random: True — бронь с произвольными данными (остальные параметры указывать не надо),
         False — бронь с конкретными данными.
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
        Получение списка с id броней.

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
