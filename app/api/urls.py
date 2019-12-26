from flask import Blueprint
from .views import EmailScheduleView, EmailTrackOpenView, EmailTrackSendView

bp = Blueprint('api', __name__)
bp.add_url_rule('/email/schedule',
                view_func=EmailScheduleView.as_view('email_schedule'))
bp.add_url_rule('/email/send-track',
                view_func=EmailTrackSendView.as_view('email_send_track'))

bp.add_url_rule('/email/open-track',
                view_func=EmailTrackOpenView.as_view('email_open_track'))
