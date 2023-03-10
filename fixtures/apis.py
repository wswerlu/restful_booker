from pytest import fixture

from api import AuthApi, BookingApi


# ---------------------------------------------- Инициализация хелперов ---------------------------------------------- #
@fixture(scope='function')
def booking_api():
    return BookingApi()


@fixture(scope='function')
def auth_api():
    return AuthApi()


# ------------------------------------- Фикстуры для подготовки тестовых данных -------------------------------------- #
@fixture(scope='function')
def create_booking(booking_api):
    """
    Создание бронирования.
    """

    return booking_api.create_booking()


@fixture(scope='function')
def create_token(auth_api):
    """
    Создание токена.
    """

    return auth_api.create_token()
