from rest_framework.permissions import BasePermission

class IsComptable(BasePermission):
    """
    Permission pour les utilisateurs ayant le rôle de Directeur.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'Directeur'

class IsGestionnaire(BasePermission):
    """
    Permission pour les utilisateurs ayant le rôle de gestionnaire.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'Gestionnaire'


class IsComptable(BasePermission):
    """
    Permission pour les utilisateurs ayant le rôle de comptable.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'Comptable'
