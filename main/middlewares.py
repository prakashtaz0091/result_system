# myapp/middleware/custom_middleware.py
from django.shortcuts import redirect
from django.urls import reverse


    



class ProtectAdminPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'admin_pages/' in request.path and not request.user.is_superuser:
            return redirect('home')

        response = self.get_response(request)
        return response
    



class ProtectTeacherPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'teacher_pages/' in request.path and request.user.is_superuser:
            return redirect('admin_view')

        response = self.get_response(request)
        return response