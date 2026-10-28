"""
config/asgi.py

ASGI = Async Server Gateway Interface. Not used by this project's simple REST API
(which runs fine on WSGI/Gunicorn), but Django generates it by default and it's
needed if you later add async features like websockets or async views.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
