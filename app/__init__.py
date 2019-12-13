import inspect
import warnings

from flask import Flask


class App(Flask):

    def _register_extension(self, name, ext):
        """register extension
        :param name: extension name
        :param ext: extension object
        """
        ext.init_app(self)
        if name not in self.extensions:
            self.extensions[name] = ext

    def load_extensions_in_module(self, module):
        def is_ext(ins):
            return not inspect.isclass(ins) and hasattr(ins, 'init_app')
        for n, ext in inspect.getmembers(module, is_ext):
            self._register_extension(n, ext)
        return self.extensions

    def ready(self):
        """
        do anything you want after initiation,
        for example register blueprint or set test_client_class for your app
        """
        pass
