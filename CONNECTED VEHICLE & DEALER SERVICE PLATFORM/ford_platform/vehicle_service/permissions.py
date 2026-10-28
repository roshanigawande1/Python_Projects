"""
vehicle_service/permissions.py

PERMISSIONS answer "what is this already-authenticated user ALLOWED to do?"
(Authentication, handled separately, answers "who IS this user?")

DRF checks permission classes automatically before your view code runs. If a
permission check fails, DRF returns 403 Forbidden without ever touching your
business logic — this is a clean way to keep authorization rules out of your views.
"""

from rest_framework.permissions import BasePermission


class IsDealerUser(BasePermission):
    """
    Example object-level permission: a user may only act on objects (Vehicle,
    ServiceAppointment, etc.) that belong to THEIR OWN dealer.

    In this demo project, we fake "which dealer does this user belong to" using a
    `dealer_id` attribute set on the user in tests/admin. In a real enterprise system,
    this would instead come from a trusted claim inside the caller's OAuth2/JWT access
    token (issued by an identity provider) — never from something the client can edit.
    """

    def has_permission(self, request, view):
        # Basic check: must be logged in at all.
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Fine-grained check: does this specific object belong to the caller's dealer?
        user_dealer_id = getattr(request.user, "dealer_id", None)
        obj_dealer_id = getattr(obj, "dealer_id", None)
        return user_dealer_id is not None and user_dealer_id == obj_dealer_id
