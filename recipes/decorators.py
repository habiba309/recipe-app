from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Redirect non-admins away from admin-only views."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        if getattr(request.user, 'role', None) != 'admin':
            messages.error(request, 'Access denied. Admins only.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
