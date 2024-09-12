# myapp/middleware/custom_middleware.py
from django.shortcuts import redirect
from django.urls import reverse


class SuperuserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is trying to log in and is authenticated
        if (request.path == reverse('login') or request.path == reverse('home')) and request.user.is_authenticated:
            # Check if the user is a superuser
            if request.user.is_superuser:
                # Redirect to the custom admin page
                return redirect('admin_view')  # Ensure this matches your view name

        response = self.get_response(request)
        return response