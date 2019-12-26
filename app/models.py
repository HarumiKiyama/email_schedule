from app.extensions import pwx
from datetime import datetime
from peewee import CharField, IntegerField, TextField, DateTimeField


class EmailLog(pwx.Model):
    SCHEDULED = 0
    IN_QUEUE = 1
    SEND_MAILGUN = 2
    SEND_FAILED = 3
    SEND_SUCCESSFULLY = 4
    OPENED = 5
    STATUS_CHOICES = (
        (SCHEDULED, 'email scheduled'),
        (IN_QUEUE, 'email in queue ready for sending'),
        (SEND_MAILGUN, 'email send to mailgun'),
        (SEND_FAILED, 'email send failed'),
        (SEND_SUCCESSFULLY, 'email send successfully'),
        (OPENED, 'email opened'),
    )

    to = CharField(max_length=50)
    body = TextField()
    subject = TextField()
    status = IntegerField(default=SCHEDULED, choices=STATUS_CHOICES)
    send_at = DateTimeField()
    email_id = CharField(max_length=100, null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        indexes = ((('email_id', 'send_at'), True), )
        table_name = 'email_logs'
