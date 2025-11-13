from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.is_admin():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def manager_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.userprofile.is_manager() or request.user.userprofile.is_admin()):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap