"""
config/urls.py

The top-level URL "table of contents" for the whole project. Django checks each
incoming request's path against this list, top to bottom, and hands it off to
whichever app/view matches first.
"""

from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def health_check(request):
    """
    A tiny endpoint that just returns {"status": "ok"}.

    This matches the readinessProbe / livenessProbe paths in k8s/deployment.yaml —
    Kubernetes calls this URL repeatedly to check "is this pod alive and ready to
    receive traffic?" If it stops responding, Kubernetes restarts the pod.
    """
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),                       # Django's built-in admin UI
    path("health/", health_check),                          # Kubernetes health checks
    path("api/v1/", include("vehicle_service.urls")),       # All our REST API endpoints
    # Adding api/v2/ later (pointing at a new urls module) is how you'd version the API
    # without breaking existing clients — see PDF Section 13, "Why API versioning?"
]
