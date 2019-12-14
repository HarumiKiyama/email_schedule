from flask.views import MethodView
from flask import request, jsonify
import datetime
from app.models import EmailLog


class EmailScheduleView(MethodView):
    def post(self):
        data = request.get_json()
        if data.get('eta') is not None:
            send_at = data['eta']
        else:
            count_down = data['count_down']
            send_at = datetime.datetime.now() + datetime.timedelta(
                **count_down)
        EmailLog.create(subject=data['subject'],
                        body=data['body'],
                        to=data['to'],
                        cc=data['cc'],
                        send_at=send_at)
        return jsonify()
