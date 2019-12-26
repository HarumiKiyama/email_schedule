import datetime

from flask.views import MethodView
from flask import request, jsonify, Response

from app.exceptions import ScheduleTimeException
from app.models import EmailLog
from app.extensions import mailext
from app.tasks import send_email


class EmailScheduleView(MethodView):
    def post(self):
        data = request.get_json()
        now = datetime.datetime.now()
        if data.get('eta') is not None:
            send_at = datetime.datetime.strptime(data['eta'],
                                                 '%Y-%m-%d %H:%M:%S')
            if send_at < now:
                raise ScheduleTimeException(
                    'schedule time:{} error'.format(send_at))
        else:
            countdown = data['countdown']
            send_at = datetime.datetime.now() + datetime.timedelta(**countdown)

        email = EmailLog.create(subject=data['subject'],
                                body=data['body'],
                                to=data['to'],
                                send_at=send_at)
        if send_at - now <= datetime.timedelta(minutes=15):
            send_email.apply_async(args=(email.id, ), eta=send_at)
        return jsonify()


class EmailTrackSendView(MethodView):
    def post(self):
        data = request.get_json()
        event_data = data['event-data']
        if event_data['event'] not in (
                'delivered',
                'failed',
        ) or not mailext.verify(**data['signature']):
            return Response(status=406)
        email_id = event_data['id']
        email = EmailLog.select().where(EmailLog.email_id == email_id).first()
        if email is None or email.status != EmailLog.SEND_MAILGUN:
            return Response(status=406)
        if event_data['event'] == 'failed':
            EmailLog.set_by_id(email.id, {'status': EmailLog.SEND_FAILED})
        else:
            EmailLog.set_by_id(
                email.id, {
                    'status': EmailLog.SEND_SUCCESSFULLY,
                    'updated_at': datetime.datetime.now()
                })
        return Response(status=200)


class EmailTrackOpenView(MethodView):
    def post(self):
        data = request.get_json()
        event_data = data['event-data']
        if event_data['event'] != 'opened' or not mailext.verify(
                **data['signature']):
            return Response(status=406)
        email_id = event_data['id']
        email = EmailLog.select().where(EmailLog.email_id == email_id).first()
        if email is None or email.status != EmailLog.SEND_SUCCESSFULLY:
            return Response(status=406)
        EmailLog.set_by_id(email.id, {
            'status': EmailLog.OPENED,
            'updated_at': datetime.datetime.now()
        })
        return Response(status=200)
