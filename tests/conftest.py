import datetime
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
def clean_db(app):
    yield
    for model in (EmailLog, ):
        model.delete().execute()


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def faker():
    return Faker()


@pytest.fixture()
def email_logs_called_mailgun(faker):
    for _ in range(10):
        send_at = datetime.datetime.strptime(str(faker.past_datetime()),
                                             '%Y-%m-%d %H:%M:%S')
        EmailLog.create(
            to=faker.email(),
            body=faker.text(),
            send_at=send_at,
            subject=faker.sentence(),
            email_id=faker.isbn13(),
            status=EmailLog.SEND_MAILGUN,
        )
    yield


@pytest.fixture()
def email_logs(faker):
    for _ in range(5):
        send_at = datetime.datetime.strptime(str(faker.future_datetime()),
                                             '%Y-%m-%d %H:%M:%S')
        EmailLog.create(
            to=faker.email(),
            body=faker.text(),
            send_at=send_at,
            subject=faker.sentence(),
        )
    for _ in range(5):
        send_at = datetime.datetime.now() + datetime.timedelta(
            minutes=faker.pyint(min_value=1, max_value=10))
        EmailLog.create(
            to=faker.email(),
            body=faker.text(),
            send_at=send_at,
            subject=faker.sentence(),
        )
    yield


# def pytest_sessionfinish(session, exitstatus):
#     models = (EmailLog, )
#     pwx.database.drop_tables(models)


def pytest_sessionstart(session):
    models = (EmailLog, )
    pwx.database.create_tables(models)
