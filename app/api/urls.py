from flask import Blueprint
from .views import EmailScheduleView, EmailTrackView

bp = Blueprint('api', __name__)
bp.add_url_rule('/email/schedule',
                view_func=EmailScheduleView.as_view('email_schedule'))
bp.add_url_rule('/email/track',
                view_func=EmailTrackView.as_view('email_track'))
