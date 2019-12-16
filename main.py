#!/usr/bin/env python3
import sys
import os

from app import create_app
from gunicorn.app.base import Application


class WSGIApplication(Application):
    def init(self, parser, opts, args):
        self.cfg.set('proc_name', 'atlas_api')
        self.cfg.set('bind', '0.0.0.0:8080')

    def load(self):
        return create_app()


def main():
    args = sys.argv[1:]
    if args[0] == 'server':
        sys.argv = ['gunicorn']
        return WSGIApplication('%(prog)s [OPTIONS]').run()
    elif args[0] == 'shell':
        _app = create_app()
        banner = '[Atlas API Console]:\n`ALTAS_ENV` is {}\nplease be careful\nthe following vars are included:\n`app` (the current app)\n'.format(  # noqa
            os.environ.get('ATLAS_ENV', 'testing'))
        ctx = {'app': _app}
        from IPython.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed(user_ns=ctx, banner1=banner)
        ipshell()
        return 0
    raise KeyError


if __name__ == '__main__':
    main()
