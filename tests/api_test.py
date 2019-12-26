import datetime

import pytest

from app.models import EmailLog
from app.exceptions import ScheduleTimeException


def test_schedule_email_by_eta(client, mocker, faker):
    from app.tasks import send_email
    mocker.patch.object(
        send_email,
        'apply_async',
    )
    data = {
        'to': faker.email(),
        'eta': str(faker.future_datetime()),
        'body': faker.text(),
        'subject': faker.sentence()
    }
    resp = client.post('/email/schedule', json=data)
    assert resp.status_code == 200
    email = EmailLog.select().first()
    assert email.to == data['to']
    assert str(email.send_at) == data['eta']
    assert email.body == data['body']


def test_schedule_email_by_eta_failed(client, faker):
    data = {
        'to': faker.email(),
        'eta': str(faker.date_time(end_datetime=datetime.datetime.now())),
        'body': faker.text(),
        'subject': faker.sentence()
    }

    with pytest.raises(ScheduleTimeException):
        client.post('/email/schedule', json=data)


def test_schedule_email_by_countdown(client, faker):
    data = {
        'to': faker.email(),
        'countdown': {
            'hours': faker.pyint(),
            'minutes': faker.pyint(),
            'seconds': faker.pyint(),
        },
        'body': faker.text(),
        'subject': faker.sentence()
    }
    resp = client.post('/email/schedule', json=data)
    assert resp.status_code == 200
    email = EmailLog.select().first()
    assert email.created_at + datetime.timedelta(
        **data['countdown']) == email.send_at


def test_email_track_open_successfully(client, mocker, faker,
                                       email_logs_called_mailgun):
    from app.api.views import mailext
    verify_mock = mocker.patch.object(mailext, 'verify', return_val=True)
    email = EmailLog.select().first()
    EmailLog.set_by_id(email.id, {
        'status': EmailLog.SEND_SUCCESSFULLY,
    })
    resp = client.post('/email/open-track',
                       json={
                           'event-data': {
                               'event': 'opened',
                               'id': email.email_id,
                           },
                           'signature': {}
                       })
    assert resp.status_code == 200
    assert EmailLog[email.id].status == EmailLog.OPENED
    assert verify_mock.called


def test_email_track_open_failed_verify(client, mocker, faker,
                                        email_logs_called_mailgun):
    from app.api.views import mailext
    verify_mock = mocker.patch.object(mailext, 'verify', return_val=False)
    resp = client.post('/email/open-track',
                       json={
                           'event-data': {
                               'event': 'opened',
                               'id': faker.isbn13(),
                           },
                           'signature': {}
                       })
    assert resp.status_code == 406
    assert verify_mock.called


def test_email_track_send_failed_can_not_find_email(client, faker, mocker,
                                                    email_logs_called_mailgun):
    from app.api.views import mailext
    verify_mock = mocker.patch.object(mailext, 'verify', return_val=True)
    resp = client.post('/email/send-track',
                       json={
                           'event-data': {
                               'event': 'delivered',
                               'id': faker.isbn13(),
                           },
                           'signature': {}
                       })
    assert resp.status_code == 406
    assert verify_mock.called


def test_email_track_send_failed(client, faker, mocker,
                                 email_logs_called_mailgun):
    from app.api.views import mailext
    verify_mock = mocker.patch.object(mailext, 'verify', return_val=True)
    email = EmailLog.select().first()
    resp = client.post('/email/send-track',
                       json={
                           'event-data': {
                               'event': 'failed',
                               'id': email.email_id,
                           },
                           'signature': {}
                       })
    assert resp.status_code == 200
    assert EmailLog[email.id].status == EmailLog.SEND_FAILED
    assert verify_mock.called


def test_email_track_send_successfully(client, faker, mocker,
                                       email_logs_called_mailgun):
    from app.api.views import mailext
    verify_mock = mocker.patch.object(mailext, 'verify', return_val=True)
    email = EmailLog.select().first()
    resp = client.post('/email/send-track',
                       json={
                           'event-data': {
                               'event': 'delivered',
                               'id': email.email_id,
                           },
                           'signature': {}
                       })
    assert resp.status_code == 200
    assert EmailLog[email.id].status == EmailLog.SEND_SUCCESSFULLY
    assert verify_mock.called
