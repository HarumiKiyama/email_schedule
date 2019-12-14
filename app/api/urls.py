from . import bp
from .views import EmailScheduleView

bp.app_url_rule('/email/schedule',
                view_func=EmailScheduleView.as_view('email_schedule'))
