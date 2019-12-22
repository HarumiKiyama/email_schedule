from celery import Celery


class Celeryext(Celery):
    def init_app(self, app):
        self.config_from_object(app.config.get_namespace('CELERY_'))
