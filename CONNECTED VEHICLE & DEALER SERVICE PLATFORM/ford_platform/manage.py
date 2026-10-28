#!/usr/bin/env python
"""
manage.py

This is the command-line tool for the whole project. Every command you run
(runserver, migrate, test, createsuperuser, makemigrations...) goes through this
file. You never need to edit it — Django generates it automatically.
"""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Did you forget to activate your virtual "
            "environment and run `pip install -r requirements.txt`?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
