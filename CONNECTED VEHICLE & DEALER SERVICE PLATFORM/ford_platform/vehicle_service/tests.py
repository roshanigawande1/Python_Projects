"""
vehicle_service/tests.py

Automated tests. Run them with:  python manage.py test

Why this matters in an interview: it proves (with code, not just talk) that
authentication is enforced and that dealer data isolation actually works.
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Dealer, Vehicle


class VehicleApiTests(APITestCase):
    def setUp(self):
        # Create two separate dealers, each with their own vehicle,
        # so we can prove they can't see each other's data.
        self.dealer_a = Dealer.objects.create(dealer_code="D001", name="Dealer A")
        self.dealer_b = Dealer.objects.create(dealer_code="D002", name="Dealer B")

        self.vehicle_a = Vehicle.objects.create(
            vin="1FTFW1E50PFA00001", model="F-150", year=2025,
            owner_id="customer-a", dealer=self.dealer_a,
        )
        self.vehicle_b = Vehicle.objects.create(
            vin="1FTFW1E50PFA00002", model="Mustang", year=2025,
            owner_id="customer-b", dealer=self.dealer_b,
        )

        User = get_user_model()
        self.user_a = User.objects.create_user(username="dealer_a_user", password="StrongPassword!")
        self.user_a.dealer_id = self.dealer_a.id  # See permissions.py note: this is a demo-only shortcut

    def test_vehicle_list_requires_authentication(self):
        """An anonymous (not logged-in) request must be rejected."""
        response = self.client.get("/api/v1/vehicles/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vehicle_list_is_scoped_to_caller_dealer(self):
        """A logged-in dealer user must only see their OWN dealer's vehicles."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/v1/vehicles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vins_returned = [v["vin"] for v in response.data["results"]]
        self.assertIn(self.vehicle_a.vin, vins_returned)
        self.assertNotIn(self.vehicle_b.vin, vins_returned)  # Dealer A must never see Dealer B's car
