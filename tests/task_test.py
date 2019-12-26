import datetime

from app.tasks import send_email, schedule_emails
from app.models import EmailLog


def test_send_email(mocker, email_logs, faker):
    from app.tasks import mailext
    return_val = {'id': faker.isbn13()}
    send_mock = mocker.patch.object(mailext,
                                    'send_email',
                                    return_value=return_val)
    email = EmailLog.select().first()
    send_email(email.id)
    assert send_mock.called == 1
    assert EmailLog[email.id].status == EmailLog.SEND_MAILGUN
    assert EmailLog[email.id].email_id == return_val['id']


def test_delay_email(mocker, email_logs, faker):
    from app.tasks import send_email
    send_mock = mocker.patch.object(
        send_email,
        'apply_async',
    )
    schedule_emails()
    now = datetime.datetime.now()
    query = EmailLog.select().where(
        EmailLog.send_at <= now + datetime.timedelta(minutes=10),
        EmailLog.status != EmailLog.IN_QUEUE)
    assert query.count() == 0
    query = EmailLog.select().where(EmailLog.status == EmailLog.IN_QUEUE,)
    assert query.count() == send_mock.call_count
