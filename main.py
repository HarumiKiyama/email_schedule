#!/usr/bin/env python3
import sys
import os

from app import create_app
from gunicorn.app.base import Application


class WSGIApplication(Application):
    def init(self, parser, opts, args):
        self.cfg.set('proc_name', 'email_schedule')
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
        banner = '[EMAIL Console]:\n`EMAIL_ENV` is {}\nplease be careful\nthe following vars are included:\n`app` (the current app)\n'.format(  # noqa
            os.environ.get('EMAIL_ENV', 'testing'))
        ctx = {'app': _app}
        from IPython.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed(user_ns=ctx, banner1=banner)
        ipshell()
        return 0
    elif args[0] == 'celery':
        create_app()
        from celery.__main__ import main as celerymain
        sys.argv = args
        sys.argv.extend(['-A', 'app.extensions:celeryapp'])
        return celerymain()
    raise KeyError


if __name__ == '__main__':
    main()
