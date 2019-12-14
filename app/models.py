from app.extensions import pwx
from datetime.datetime import now
from peewee import CharField, IntegerField, TextField, DatetimeField


class EmailLog(pwx.Model):
    to = CharField(max_length=50)
    body = TextField()
    status = IntegerField()
    send_at = DatetimeField()
    created_at = DatetimeField(default=now)
    updated_at = DatetimeField(default=now)
