#!/usr/bin/env python3
import pytest
import sys
import os
from app import create_app


class AppPlugins:
    def pytest_load_initial_conftests(early_config, parser, args):
        create_app()


def main():
    os.environ['EMAIL_ENV'] = 'testing'
    args = sys.argv[1:]
    sys.exit(pytest.main(['-v', *args], plugins=[AppPlugins]))


if __name__ == '__main__':
    main()
