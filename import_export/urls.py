from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', 
        include(
            [
                path('import/students/', login_required(views.import_students_view), name="import_students_view"),
            ]

        ) 
        ),

]