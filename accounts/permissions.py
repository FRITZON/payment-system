from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import UserRole

class IsAdmin(permissions.BasePermission):    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("Vous devez être authentifié pour accéder à cette ressource.")

        if request.user.role != UserRole.ADMIN:
            raise PermissionDenied("Accès refusé : vous devez être un administrateur.")

        return True

class IsOperator(permissions.BasePermission):    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("Vous devez être authentifié pour accéder à cette ressource.")

        if request.user.role != UserRole.OPERATOR:
            raise PermissionDenied("Accès refusé : vous devez être un opérateur.")

        return True

class IsSubscriber(permissions.BasePermission):    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("Vous devez être authentifié pour accéder à cette ressource.")

        if request.user.role != UserRole.SUBSCRIBER:
            raise PermissionDenied("Accès refusé : vous devez être un abonné.")

        return True
