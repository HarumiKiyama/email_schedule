from peewee import Model
from playhouse import db_url
from werkzeug.utils import cached_property


class Peeweext:
    def __init__(self, ns='PW_'):
        self.ns = ns

    def init_app(self, app):
        opts = app.config.get_namespace(self.ns)
        conn_params = opts.get('conn_params', {})
        self.database = db_url.connect(opts['db_url'], **conn_params)

    @cached_property
    def Model(self):
        class BaseModel(Model):
            class Meta:
                database = self.database

        return BaseModel

    def connect_db(self):
        if self.database.is_closed():
            self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed():
            self.database.close()
