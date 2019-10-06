from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # 只允许创建者去修改
    def has_object_permission(self, request, view, obj):
        # 任何request都有【读】的权限
        if request.method in permissions.SAFE_METHODS:
            return True
        # 只有创建者才有【写】的权限
        return obj.owner == request.user