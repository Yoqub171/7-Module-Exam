from rest_framework import permissions
from datetime import datetime


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    

class IsJohnBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.full_name == 'john':
            return False
        return True
    

class JohnReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.full_name == 'john':
            if request.method in ['POST', 'DELETE' ,'PUT', 'PATCH']:
                return False
            return True


class MondayFriday(permissions.BasePermission):
    def has_permission(self, request, view):
        today = datetime.today().weekday()
        return today < 5
        

class CanReadPremiumCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
    
class IsEvenYear(permissions.BasePermission):
    def has_permission(self, request, view):
        current_year = datetime.now().year
        if current_year % 2 == 0:
            return True
        return False
    
class LoginOnlySuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class PutPatchOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['PUT', 'PATCH']