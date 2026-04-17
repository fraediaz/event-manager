from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEventOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        return getattr(obj, 'creator_id', None) == request.user.id


class IsAttendanceOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return getattr(obj, 'user_id', None) == request.user.id