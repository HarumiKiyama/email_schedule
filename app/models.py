from app.extensions import pwx
from datetime import datetime
from peewee import CharField, IntegerField, TextField, DateTimeField


class EmailLog(pwx.Model):
    to = CharField(max_length=50)
    body = TextField()
    status = IntegerField()
    send_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
