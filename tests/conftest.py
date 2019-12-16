import pytest
from faker import Faker
from app import create_app
from app.models import EmailLog
from app.extensions import pwx


@pytest.fixture(scope='session')
def app():
    _app = create_app()
    return _app


@pytest.fixture(autouse=True)
def db(app):
    models = (EmailLog, )
    pwx.database.create_tables(models)
    yield
    for model in models:
        model.delete().execute()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def fake():
    return Faker()


def pytest_sessionfinish(session, exitstatus):
    models = (EmailLog, )
    pwx.database.drop_tables(models)
