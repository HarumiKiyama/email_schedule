from app.extensions import pwx
from datetime import datetime
from peewee import CharField, IntegerField, TextField, DateTimeField


class EmailLog(pwx.Model):
    SCHEDULED = 0
    IN_QUEUE = 1
    SEND_FAILED = 2
    SEND_SUCCESSFULLY = 3
    OPENED = 4
    STATUS_CHOICES = (
        (SCHEDULED, 'email scheduled'),
        (IN_QUEUE, 'email in queue ready for sending'),
        (SEND_FAILED, 'email send failed'),
        (SEND_SUCCESSFULLY, 'email send successfully'),
        (OPENED, 'email opened'),
    )

    to = CharField(max_length=50)
    body = TextField()
    status = IntegerField(default=SCHEDULED, choices=STATUS_CHOICES)
    send_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
