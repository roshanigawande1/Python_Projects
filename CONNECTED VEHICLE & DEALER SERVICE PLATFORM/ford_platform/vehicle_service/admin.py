"""
vehicle_service/admin.py

Registering a model here makes it manageable through Django's built-in admin panel
at /admin/ — a free CRUD UI you get without writing any HTML. Extremely useful for
quickly adding test data (dealers, vehicles) while developing, without needing a
separate frontend.
"""

from django.contrib import admin
from .models import Dealer, Vehicle, ServiceAppointment, DiagnosticCode


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ["dealer_code", "name"]
    search_fields = ["dealer_code", "name"]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["vin", "model", "year", "owner_id", "dealer"]
    list_filter = ["dealer", "year"]
    search_fields = ["vin", "owner_id"]


@admin.register(ServiceAppointment)
class ServiceAppointmentAdmin(admin.ModelAdmin):
    list_display = ["id", "vehicle", "dealer", "scheduled_at", "status"]
    list_filter = ["status", "dealer"]


@admin.register(DiagnosticCode)
class DiagnosticCodeAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "code", "severity", "observed_at"]
    list_filter = ["severity"]
