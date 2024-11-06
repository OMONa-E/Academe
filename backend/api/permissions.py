from rest_framework import permissions

# CEO Auth
# -------------------------------------
class IsCEO(permissions.BasePermission):
    '''
    Custom permission to only allow users with the role of CEO to Access
    '''
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'CEO')

# Employer Auth
# -------------------------------------
class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Employer')

# Employee Auth
# -------------------------------------
class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Employee')

# CEO Or Employer Auth
# -------------------------------------
class IsEmployerOrCEO(permissions.BasePermission):
    '''
    Custom permission to only allow users with the role of CEO or Employer to Access
    '''
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role in ['CEO', 'Employer'])
    
# CEO or Employer or Employee Auth
# -------------------------------------
class IsEmployerOrEmployeeOrCEO(permissions.BasePermission):
    '''
    Custom permission to only allow users with the role of CEO or Employer to Access
    '''
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role in ['CEO', 'Employee', 'Employer'])