# Автотесты для API [Restful-Booker](http://restful-booker.herokuapp.com/) ([документация](http://restful-booker.herokuapp.com/apidoc/index.html))

## Что реализовано

В рамках проекта реализовано:

1. API автотесты с использованием pytest + requests
2. Автоматическая локальная проверка линтером flake8 при коммитах с помощью pre-commit:
   * [yaml файл](https://github.com/wswerlu/restful_booker/blob/main/.pre-commit-config.yaml)
   * [документация pre-commit](https://pre-commit.com/)
3. Автоматическая проверка кода линтером flake8 при push и pull request в любую ветку проекта:
   * [yaml файл](https://github.com/wswerlu/restful_booker/blob/main/.github/workflows/flake8.yml)
   * [actions](https://github.com/wswerlu/restful_booker/actions/workflows/flake8.yml)
4. Ручной запуск тестов на сервере github`а:
   * [yaml файл](https://github.com/wswerlu/restful_booker/blob/main/.github/workflows/pytest.yml)
   * [actions](https://github.com/wswerlu/restful_booker/actions/workflows/pytest.yml)
5. Генерация allure отчета с помощью github pages:
   * отчет отображается на странице: https://wswerlu.github.io/restful_booker/

## Ручной запуск тестов

Для ручного запуска тестов необходимо:

1. Перейти на страницу: https://github.com/wswerlu/restful_booker/actions/workflows/pytest.yml
2. Нажать на дропдаун **Run workflow** справа
3. Нажать на кнопку **Run workflow**
4. Дождаться завершения прогона тестов
5. Дождаться завершения процесса сборки и деплоя сайта (actions: [pages build and deployment](https://github.com/wswerlu/restful_booker/actions/workflows/pages/pages-build-deployment))
6. Открыть отчет по ссылке (**открывать в режиме инкогнито**): https://wswerlu.github.io/demo_web_shop/