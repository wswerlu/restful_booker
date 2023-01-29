from pytest import fixture

from api import BookingApi


# ---------------------------------------------- Инициализация хелперов ---------------------------------------------- #
@fixture(scope='function')
def booking_api():
    return BookingApi()


# ------------------------------------- Фикстуры для подготовки тестовых данных -------------------------------------- #
@fixture(scope='function')
def create_booking(booking_api):
    """
    Создание бронирования.
    """

    return booking_api.create_booking()
