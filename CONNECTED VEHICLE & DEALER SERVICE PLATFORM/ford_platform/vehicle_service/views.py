"""
vehicle_service/views.py

VIEWS (here, ViewSets) contain the actual logic that runs when a request hits an
endpoint: fetch data, apply business rules, save changes, return a response.

We use DRF's ModelViewSet / ReadOnlyModelViewSet, which automatically implement the
standard CRUD operations (list, retrieve, create, update, delete) for a model, wired
up to a router (see urls.py) — this is why DRF is faster to build with than plain Django.

IMPORTANT PATTERN — data isolation between dealers:
Every `get_queryset()` below filters results down to only the rows belonging to the
CALLER's dealer. This is what stops Dealer A from ever seeing Dealer B's vehicles,
even if they guess a valid ID — the row simply isn't in their queryset, so DRF
returns 404 Not Found instead of leaking someone else's data.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Dealer, Vehicle, ServiceAppointment, DiagnosticCode
from .serializers import (
    DealerSerializer,
    VehicleSerializer,
    ServiceAppointmentSerializer,
    DiagnosticCodeSerializer,
)


def _caller_dealer_id(request):
    """
    Helper: figure out which dealer the logged-in user belongs to.

    In this learning project, we read it off request.user.dealer_id (set manually,
    e.g. in the Django admin or in tests). In a real production system this value
    would come from a verified claim inside the caller's access token instead.
    """
    return getattr(request.user, "dealer_id", None)


class DealerViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only: /api/v1/dealers/  and  /api/v1/dealers/{id}/"""
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [IsAuthenticated]


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only: dealers look up vehicle info but don't create/edit vehicles through
    this API in our simplified example (that would typically happen via a separate
    vehicle-registration system).

    select_related("dealer") is a performance optimization: it tells the ORM to fetch
    the related Dealer row in the SAME database query (a SQL JOIN) instead of firing
    a second query every time we access vehicle.dealer — avoids the classic "N+1
    query" problem.
    """
    queryset = Vehicle.objects.select_related("dealer").all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dealer_id = _caller_dealer_id(self.request)
        return super().get_queryset().filter(dealer_id=dealer_id)

    @action(detail=True, methods=["get"])
    def diagnostics(self, request, pk=None):
        """
        Custom extra endpoint: GET /api/v1/vehicles/{id}/diagnostics/
        Returns all diagnostic codes for one specific vehicle.
        `@action` is how DRF lets you add endpoints beyond the standard CRUD set.
        """
        vehicle = self.get_object()  # Reuses get_queryset() above, so dealer-scoping still applies
        codes = vehicle.diagnostic_codes.all()
        serializer = DiagnosticCodeSerializer(codes, many=True)
        return Response(serializer.data)


class ServiceAppointmentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD: /api/v1/appointments/
    Dealers can create, view, update, and cancel appointments for their own vehicles.
    """
    queryset = ServiceAppointment.objects.select_related("vehicle", "dealer").all()
    serializer_class = ServiceAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dealer_id = _caller_dealer_id(self.request)
        return super().get_queryset().filter(dealer_id=dealer_id)


class DiagnosticCodeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only: /api/v1/diagnostics/"""
    queryset = DiagnosticCode.objects.select_related("vehicle").all()
    serializer_class = DiagnosticCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dealer_id = _caller_dealer_id(self.request)
        return super().get_queryset().filter(vehicle__dealer_id=dealer_id)
