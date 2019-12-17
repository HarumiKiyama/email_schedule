import inspect
from flask import Flask
from flasgger import Swagger
import os
import sys
from werkzeug.utils import import_string
from flask_cors import CORS
from app.exceptions import ConfigException


class Config(dict):
    def __init__(self, root_path, defaults=None):
        super().__init__(defaults or {})
        self.root_path = root_path

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def get_namespace(self, namespace, lowercase=True, trim_namespace=True):
        rv = {}
        for k, v in self.items():
            if not k.startswith(namespace):
                continue
            if trim_namespace:
                key = k[len(namespace):]
            else:
                key = k
            if lowercase:
                key = key.lower()
            rv[key] = v
        return rv

    def __repr__(self):
        return f'<{self.__class__.__name__}, {dict.__repr__(self)}>'


class App(Flask):
    def _register_extension(self, name, ext):
        ext.init_app(self)
        if name in self.extensions:
            raise ConfigException(f'extension duplicated: {name}')
        self.extensions[name] = ext

    def load_extensions_in_module(self, module):
        def is_ext(ins):
            return not inspect.isclass(ins) and hasattr(ins, 'init_app')

        for n, ext in inspect.getmembers(module, is_ext):
            self._register_extension(n, ext)

    def ready(self):
        from app.api import bp
        from app.extensions import pwx
        self.before_request(pwx.connect_db)
        self.teardown_request(pwx.close_db)
        self.register_blueprint(bp)


_app = None


def create_app(root_path=None):
    global _app
    if _app is not None:
        return _app
    if root_path is None:
        root_path = os.getcwd()
    sys.path.append(root_path)
    env = os.environ.get('EMAIL_ENV', 'testing')
    config = import_string('configs.{}'.format(env))

    _app = App(__name__, root_path=root_path)
    CORS(_app)
    Swagger(_app)
    _app.config.from_object(config)
    _app.load_extensions_in_module(import_string('app.extensions'))
    _app.ready()
    _app.app_context().push()
    return _app
