from flask import Blueprint
from .views import EmailScheduleView

bp = Blueprint('api', __name__)
bp.add_url_rule('/email/schedule',
                view_func=EmailScheduleView.as_view('email_schedule'))
