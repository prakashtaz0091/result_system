from django.shortcuts import redirect
def has_to_be_admin(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        return function(request, *args, **kwargs)
    return wrapper