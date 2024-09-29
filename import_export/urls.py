from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', 
        include(
            [
                path('import/students/', login_required(views.import_students_view), name="import_students_view"),
                path('export/students/', login_required(views.export_student_data_to_excel_view), name="export_student_data_to_excel_view"),
            ]

        ) 
        ),

]