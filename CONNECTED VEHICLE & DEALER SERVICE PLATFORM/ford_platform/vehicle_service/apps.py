"""
vehicle_service/apps.py

Every Django "app" (a self-contained module of functionality) needs a small config
class like this. Django uses it to identify the app internally. You rarely edit
this file — it's mostly boilerplate.
"""

from django.apps import AppConfig


class VehicleServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vehicle_service"
