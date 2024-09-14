from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('school-admin/', views.admin_view, name='admin_view'),

    path('add_students/', views.add_students, name='add_students'),
    path('student/update/<int:pk>/', login_required(views.StudentUpdateView.as_view()), name='student_update'),
    path('student/delete/<int:pk>/', login_required(views.StudentDeleteView.as_view()), name='student_delete'),


    #admin
    #teachers
    path('teachers/', login_required(views.TeacherListView.as_view()), name='teachers_view'),
    path('teachers/create/', login_required(views.TeacherCreateView.as_view()), name='teachers_create_view'),
    path('teachers/update/<int:pk>/', login_required(views.TeacherUpdateView.as_view()), name='teacher_update_view'),
    path('teachers/delete/<int:pk>/', login_required(views.TeacherDeleteView.as_view()), name='teacher_delete_view'),

    #grades
    path('grades/', login_required(views.GradeListView.as_view()), name='grades_view'),
    path('grades/create/', login_required(views.GradeCreateView.as_view()), name='grades_create_view'),
    path('grades/update/<int:pk>/', login_required(views.GradeUpdateView.as_view()), name='grades_update_view'),
    path('grades/delete/<int:pk>/', login_required(views.GradeDeleteView.as_view()), name='grades_delete_view'),


    #subjects
    path('subjects/', login_required(views.SubjectListView.as_view()), name='subjects_view'),
    path('subjects/create/', login_required(views.SubjectCreateView.as_view()), name='subjects_create_view'),
    path('subjects/update/<int:pk>/', login_required(views.SubjectUpdateView.as_view()), name='subjects_update_view'),
    path('subjects/delete/<int:pk>/', login_required(views.SubjectDeleteView.as_view()), name='subjects_delete_view'),



    #exams
    path('exams/', login_required(views.ExamListView.as_view()), name='exams_view'),
    path('exams/create/', login_required(views.ExamCreateView.as_view()), name='exams_create_view'),
    path('exams/update/<int:pk>/', login_required(views.ExamUpdateView.as_view()), name='exams_update_view'),
    path('exams/delete/<int:pk>/', login_required(views.ExamDeleteView.as_view()), name='exams_delete_view'),


]