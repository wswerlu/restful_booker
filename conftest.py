from importlib import import_module

from utils.helpers import get_fixtures

pytest_plugins = get_fixtures()


def pytest_generate_tests(metafunc):
    for fixture_name in metafunc.fixturenames:
        if fixture_name.startswith('data_'):
            module, data = fixture_name[5:].split('_')
            testdata = load_from_module(module, data)
            metafunc.parametrize(fixture_name, testdata, ids=[str(x[-1]) for x in testdata])


def load_from_module(module, data):
    return getattr(import_module(f'data.parameterization.{module}'), data)
