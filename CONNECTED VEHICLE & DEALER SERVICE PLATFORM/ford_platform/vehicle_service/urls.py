"""
vehicle_service/urls.py

Maps URL paths to ViewSets. DRF's `DefaultRouter` looks at each registered ViewSet
and AUTOMATICALLY generates the standard set of RESTful URLs for it:

  router.register("vehicles", VehicleViewSet)  creates:
    GET    /vehicles/            -> list
    POST   /vehicles/            -> create   (not available here since VehicleViewSet is read-only)
    GET    /vehicles/{id}/       -> retrieve
    PUT    /vehicles/{id}/       -> update
    PATCH  /vehicles/{id}/       -> partial_update
    DELETE /vehicles/{id}/       -> destroy

This is why ViewSets + routers are faster to build with than writing each URL by hand.
"""

from rest_framework.routers import DefaultRouter
from .views import (
    DealerViewSet,
    VehicleViewSet,
    ServiceAppointmentViewSet,
    DiagnosticCodeViewSet,
)

router = DefaultRouter()
router.register("dealers", DealerViewSet, basename="dealer")
router.register("vehicles", VehicleViewSet, basename="vehicle")
router.register("appointments", ServiceAppointmentViewSet, basename="appointment")
router.register("diagnostics", DiagnosticCodeViewSet, basename="diagnostic")

# config/urls.py includes this list under the "api/v1/" prefix, so the final paths
# end up as e.g. /api/v1/vehicles/
urlpatterns = router.urls
