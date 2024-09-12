from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('school-admin/', views.admin_view, name='admin_view'),
    path('add_students/', views.add_students, name='add_students'),
]