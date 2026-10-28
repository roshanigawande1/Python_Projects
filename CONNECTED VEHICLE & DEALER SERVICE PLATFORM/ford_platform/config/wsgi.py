"""
config/wsgi.py

WSGI = Web Server Gateway Interface — the standard way Python web apps talk to a
production web server. Gunicorn (see Dockerfile's CMD) imports `application` from
this file and uses it to actually serve HTTP requests.

You don't need to touch this file — it's boilerplate Django generates automatically.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
