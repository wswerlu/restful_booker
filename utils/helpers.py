from datetime import date, datetime, timedelta
from glob import glob
from json import load
from os.path import join
from pathlib import Path
from platform import system
from random import choice, randint

from allure import step
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from mimesis.exceptions import SchemaError
from requests import Response

from utils.generated_test_data import UserData


def get_fixtures():
    fixtures = join(Path(__file__).parent.parent, 'fixtures')
    file_path = []
    for file in glob(f'{fixtures}/*'):
        file = file.split('/') if system().lower() in ['linux', 'darwin'] else file.split('\\')
        file = file[-1].split('.')[0]
        if file not in ['__init__', '__pycache__']:
            file_path.append(f'fixtures.{file}')
    return file_path


def validate_json(response: Response, name: str):
    with open(Path(__file__).parent.parent / 'json_schema' / f'{name}.json') as file:
        json_file = load(file)
    try:
        validate(instance=response, schema=json_file)
        return True
    except SchemaError:
        print('Схема содержит ошибку')
    except ValidationError as e:
        print('Ошибка', e)
    except Exception as e:
        print(e)
    return False


@step('Проверка ответа API - {name}')
def json_schema_asserts(response: Response, name: str):
    """
    Метод проверки достоверности результата теста на основе схемы json

    :param response: Ответ от сервера
    :param name: Имя схемы JSON
    """
    assert validate_json(response, name), f'Ошибка при валидации схемы - {name}'


def get_booking_data():
    checkin = date.today() + timedelta(days=randint(0, 366))
    checkout = checkin + timedelta(days=randint(0, 366))

    return {
        'firstname': UserData().firstname(),
        'lastname': UserData().lastname(),
        'totalprice': randint(1, 100000),
        'depositpaid': choice([True, False]),
        'checkin': str(checkin),
        'checkout': str(checkout),
        'additionalneeds': choice(['Breakfast', 'Lunch', 'Dinner']),
    }


def get_updated_date(old_date: str, delta: int = 1):
    new_date = datetime.strptime(old_date, '%Y-%m-%d') + timedelta(days=delta)

    return datetime.strftime(new_date, '%Y-%m-%d')
