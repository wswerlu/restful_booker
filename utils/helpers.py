from glob import glob
from json import load
from os.path import join
from pathlib import Path
from platform import system

from allure import step
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from mimesis.exceptions import SchemaError
from requests import Response


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
