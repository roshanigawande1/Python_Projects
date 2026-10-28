"""
vehicle_service/serializers.py

SERIALIZERS are the boundary between the outside world (JSON over HTTP) and your
internal Python/database objects.

Two jobs, both important:
  1. OUTPUT: turn a Vehicle/Dealer/etc. Python object into JSON to send back to the client.
  2. INPUT: take incoming JSON from a client, VALIDATE it (types, required fields, custom
     rules), and turn it into a clean Python object ready to save to the database.

This is your main defense against bad/malicious input — never trust data from a client
just because it "looks" like a valid vehicle ID.
"""

from rest_framework import serializers
from .models import Dealer, Vehicle, ServiceAppointment, DiagnosticCode


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ["id", "dealer_code", "name"]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["id", "vin", "model", "year", "owner_id", "dealer"]

    def validate_vin(self, value):
        """
        Field-level validation: DRF automatically calls validate_<fieldname> for any
        field you define here. This is where you'd add extra rules beyond "is it a string".
        """
        if len(value) != 17:
            # Real VINs are always exactly 17 characters.
            raise serializers.ValidationError("VIN must be exactly 17 characters long.")
        return value


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAppointment
        fields = ["id", "vehicle", "dealer", "scheduled_at", "status", "created_at"]
        read_only_fields = ["created_at"]  # Clients can't set this — the DB sets it automatically

    def validate(self, attrs):
        """
        Object-level validation: runs after individual fields pass, lets you check
        RELATIONSHIPS between fields. Here: you can't book an appointment for a vehicle
        at a dealer that doesn't actually service that vehicle.
        """
        vehicle = attrs.get("vehicle") or getattr(self.instance, "vehicle", None)
        dealer = attrs.get("dealer") or getattr(self.instance, "dealer", None)
        if vehicle and dealer and vehicle.dealer_id != dealer.id:
            raise serializers.ValidationError(
                "This vehicle is not serviced by the selected dealer."
            )
        return attrs


class DiagnosticCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticCode
        fields = ["id", "vehicle", "code", "severity", "observed_at"]
