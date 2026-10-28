"""
vehicle_service/models.py

MODELS = your database tables, written as Python classes.

Each class below becomes one table. Each attribute (e.g. `vin = models.CharField(...)`)
becomes one column in that table. Django's ORM (Object-Relational Mapper) reads these
classes and knows how to translate Python code like `Vehicle.objects.filter(year=2025)`
into real SQL for whichever database you're using (SQLite locally, PostgreSQL in
production) — you never write raw SQL yourself.

After changing this file, you must run:
    python manage.py makemigrations   (Django writes a "diff" describing the change)
    python manage.py migrate          (Django applies that diff to the real database)
"""

from django.db import models


class Dealer(models.Model):
    """One row per car dealership."""

    # unique=True -> no two dealers can share the same code (enforced by the database itself)
    dealer_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        # Controls how a Dealer object is displayed (e.g. in the admin panel dropdown)
        return f"{self.dealer_code} - {self.name}"


class Vehicle(models.Model):
    """One row per physical vehicle."""

    # db_index=True -> the database keeps a fast lookup index for this column,
    # because we'll frequently search/filter vehicles by VIN or owner.
    vin = models.CharField(max_length=17, unique=True, db_index=True)
    model = models.CharField(max_length=80)
    year = models.PositiveSmallIntegerField()
    owner_id = models.CharField(max_length=64, db_index=True)

    # ForeignKey = "this vehicle belongs to exactly one dealer".
    # on_delete=models.PROTECT means: Django will REFUSE to delete a Dealer if any
    # Vehicle still points to it — protects you from accidentally orphaning data.
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT, related_name="vehicles")

    def __str__(self):
        return f"{self.vin} ({self.model} {self.year})"


class ServiceAppointment(models.Model):
    """One row per service booking (e.g. 'bring the car in for an oil change')."""

    STATUS_CHOICES = [
        ("REQUESTED", "Requested"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="appointments")
    # on_delete=CASCADE here means: if a Vehicle is deleted, delete its appointments too
    # (unlike Dealer above, which we protect against deletion).
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT, related_name="appointments")
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="REQUESTED")
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set once, when the row is created

    def __str__(self):
        return f"Appt #{self.pk} - {self.vehicle.vin} - {self.status}"


class DiagnosticCode(models.Model):
    """One row per diagnostic trouble code (DTC) reported by a vehicle."""

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="diagnostic_codes")
    code = models.CharField(max_length=32)          # e.g. "P0301" (a real-world DTC format)
    severity = models.CharField(max_length=20)       # e.g. "LOW", "MEDIUM", "HIGH"
    observed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.vehicle.vin} - {self.code} ({self.severity})"
