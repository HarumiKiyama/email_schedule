from flask.views import MethodView
from flask import request, jsonify
import datetime
from app.models import EmailLog


class EmailScheduleView(MethodView):
    def post(self):
        data = request.get_json()
        if data.get('eta') is not None:
            # TODO: check whether eta is greater than today
            send_at = data['eta']
        else:
            countdown = data['countdown']
            send_at = datetime.datetime.now() + datetime.timedelta(
                **countdown)
        EmailLog.create(subject=data['subject'],
                        body=data['body'],
                        to=data['to'],
                        send_at=send_at)
        return jsonify()
