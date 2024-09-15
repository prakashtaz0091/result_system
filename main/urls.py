from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .decorators import has_to_be_admin
from django.urls import include

urlpatterns = [



    #teachers pages ****************************************************************************************
    #teachers pages ****************************************************************************************
    
    path("teacher_pages/",

        include(
            [
                path('', views.home, name='home'),

                path('students/', views.students, name='students'),
                path('student/update/<int:pk>/', login_required(views.StudentUpdateView.as_view()), name='student_update'),
                path('student/delete/<int:pk>/', login_required(views.StudentDeleteView.as_view()), name='student_delete'),

                #subjects
                path('teacher/subjects/', views.subjects_view, name='teachers_subjects_view'),
            ]
        )    
         
         
         
    ),

    #teachers pages ****************************************************************************************
    #teachers pages ****************************************************************************************










    #admin ******************************************************************************************************
    #admin ******************************************************************************************************
    path("admin_pages/",
        include(
            [
                path('school-admin/', views.admin_view, name='admin_view'),

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


                #papers
                path('papers/', login_required(views.ExamPaperListView.as_view()), name='papers_view'),
                path('papers/create/', login_required(views.ExamPaperCreateView.as_view()), name='papers_create_view'),
                path('papers/update/<int:pk>/', login_required(views.ExamPaperUpdateView.as_view()), name='papers_update_view'),
                path('papers/delete/<int:pk>/', login_required(views.ExamPaperDeleteView.as_view()), name='papers_delete_view'),  
            ]
        )
        
        
    )

    #admin ******************************************************************************************************
    #admin ******************************************************************************************************
    




]