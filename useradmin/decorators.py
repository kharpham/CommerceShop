from django.contrib import messages
from django.shortcuts import redirect

def admin_required(view_function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.warning(request, "You are not authorized to access this page.")
            return redirect('userauths:sign-in')
        return view_function(request, *args, **kwargs)
    return wrapper