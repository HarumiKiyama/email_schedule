from flask.views import MethodView
from flask import request, jsonify
import datetime
from app.models import EmailLog
from app.extensions import emailext


class EmailScheduleView(MethodView):
    def post(self):
        data = request.get_json()
        if data.get('eta') is not None:
            # TODO: check whether eta is greater than today
            send_at = data['eta']
        else:
            countdown = data['countdown']
            send_at = datetime.datetime.now() + datetime.timedelta(**countdown)
        EmailLog.create(subject=data['subject'],
                        body=data['body'],
                        to=data['to'],
                        send_at=send_at)
        return jsonify()


class EmailTrackView(MethodView):
    def post(self):
        data = request.get_json()
        if not emailext.verify(**data['signature']):
            return jsonify()
        event_data = data['event-data']
        email_id = event_data['id']
        email = EmailLog.select().where(EmailLog.email_id == email_id).first()
        if email is not None:
            pass
