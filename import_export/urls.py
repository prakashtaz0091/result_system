from django.urls import path
from . import views

urlpatterns = [
    path('import/students/', views.import_students_view, name="import_students_view"),
]