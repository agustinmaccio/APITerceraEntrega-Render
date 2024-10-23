from rest_framework import permissions
class IsDepositosGlobales(permissions.BasePermission):
    """
    Permiso para usuarios con rol 'Depósitos Globales'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'depositos_globales'
class IsDepositosProveedores(permissions.BasePermission):
    """
    Permiso para usuarios con rol 'Depósitos Proveedores'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'depositos_proveedores'