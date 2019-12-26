from app.extensions import mailext, celeryapp
from app.models import EmailLog
import datetime


@celeryapp.task
def send_email(email_log_id):
    email = EmailLog[email_log_id]
    rv = mailext.send_email(email.to, email.subject, email.body)
    email_id = rv['id']
    EmailLog.set_by_id(email_log_id, {
        'email_id': email_id,
        'status': EmailLog.SEND_MAILGUN,
        'updated_at': datetime.datetime.now()
    })


#############
# cron jobs #
#############


@celeryapp.task
def schedule_emails():
    now = datetime.datetime.now()
    limit_time = now + datetime.timedelta(minutes=10)
    email_objs = EmailLog.select().where(EmailLog.status == EmailLog.SCHEDULED,
                                         EmailLog.send_at <= limit_time)
    for i in email_objs:
        EmailLog.set_by_id(i.id, {
            'status': EmailLog.IN_QUEUE,
            'updated_at': datetime.datetime.now()
        })
        send_email.apply_async(args=(i.id, ), eta=i.send_at)
