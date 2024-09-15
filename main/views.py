from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Grade, Subject, Exam, ExamPaper
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .import forms
from django.contrib.auth.models import User
from .decorators import has_to_be_admin







@login_required
@has_to_be_admin
def admin_view(request):
    return render(request, 'main/admin/home.html')


@login_required
def home(request):
    return render(request, 'main/home.html')



"""
Teacher Views
"""

@login_required
def students(request):
    """
    view to add students
    """

    if request.method == 'POST':
        form_data = request.POST
        roll_no = form_data['student_roll_no']
        name = form_data['student_name'].title()

        Student.objects.create(roll_no=roll_no, name=name, grade=request.user.class_teacher)
        
        return redirect('students')
        


    class_name = request.user.class_teacher

    if class_name is not None:
        students = Student.objects.filter(grade=class_name).order_by('roll_no')
        context = {
            'class': class_name,
            'students': students
        }
    else:
        context = {
            'class': "N/A",
            'students': []
        }

    return render(request, 'main/teacher/students.html', context)



class StudentUpdateView(UpdateView):
    model = Student
    form_class = forms.StudentForm
    template_name = 'main/teacher/student_update.html'
    success_url = reverse_lazy('students')  # Redirect URL after successful update.
    


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'main/teacher/student_confirm_delete.html'
    success_url = reverse_lazy('students')  # Redirect URL after successful deletion.




"""
Grade Views
"""

class GradeListView(ListView):
    model = Grade
    template_name = 'main/admin/grade_list.html'
    context_object_name = 'grades'


class GradeCreateView(CreateView):
    model = Grade
    form_class = forms.GradeForm
    template_name = 'main/admin/grade_create.html'
    success_url = reverse_lazy('grades_view')


class GradeUpdateView(UpdateView):
    model = Grade
    form_class = forms.GradeForm
    template_name = 'main/admin/grade_update.html'
    success_url = reverse_lazy('grades_view')


class GradeDeleteView(DeleteView):
    model = Grade
    template_name = 'main/admin/grade_confirm_delete.html'
    success_url = reverse_lazy('grades_view')
    context_object_name = 'grade'



"""
Teacher Views
"""
class TeacherListView(ListView):
    model = User
    template_name = 'main/admin/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        # Exclude superusers from the queryset
        return User.objects.filter(is_superuser=False)
    


class TeacherCreateView(CreateView):
    model = User
    form_class = forms.TeacherForm
    template_name = 'main/admin/teacher_create.html'
    success_url = reverse_lazy('teachers_view')


class TeacherUpdateView(UpdateView):
    model = User
    form_class = forms.TeacherForm
    template_name = 'main/admin/teacher_update.html'
    success_url = reverse_lazy('teachers_view')


class TeacherDeleteView(DeleteView):
    model = User
    template_name = 'main/admin/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers_view')
    context_object_name = 'teacher'



"""
Subject Views
"""
class SubjectListView(ListView):
    model = Subject
    template_name = 'main/admin/subject_list.html'
    context_object_name = 'subjects'



class SubjectCreateView(CreateView):
    model = Subject
    form_class = forms.SubjectForm
    template_name = 'main/admin/subject_create.html'
    success_url = reverse_lazy('subjects_view')



class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = forms.SubjectForm
    template_name = 'main/admin/subject_update.html'
    success_url = reverse_lazy('subjects_view')


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'main/admin/subject_confirm_delete.html'
    success_url = reverse_lazy('subjects_view')
    context_object_name = 'subject'





"""
Exam Views
"""
class ExamListView(ListView):
    model = Exam
    template_name = 'main/admin/exam_list.html'
    context_object_name = 'exams'



class ExamCreateView(CreateView):
    model = Exam
    form_class = forms.ExamForm
    template_name = 'main/admin/exam_create.html'
    success_url = reverse_lazy('exams_view')



class ExamUpdateView(UpdateView):
    model = Exam
    form_class = forms.ExamForm
    template_name = 'main/admin/exam_update.html'
    success_url = reverse_lazy('exams_view')



class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'main/admin/exam_confirm_delete.html'
    success_url = reverse_lazy('exams_view')
    context_object_name = 'exam'




"""
Exam Papers
"""
class ExamPaperListView(ListView):
    model = ExamPaper
    template_name = 'main/admin/exam_papers_list.html'
    context_object_name = 'exam_papers'


class ExamPaperCreateView(CreateView):
    model = ExamPaper
    form_class = forms.ExamPaperForm
    template_name = 'main/admin/exam_papers_create.html'
    success_url = reverse_lazy('papers_view')



class ExamPaperUpdateView(UpdateView):
    model = ExamPaper
    form_class = forms.ExamPaperForm
    template_name = 'main/admin/exam_papers_update.html'
    success_url = reverse_lazy('papers_view')



class ExamPaperDeleteView(DeleteView):
    model = ExamPaper
    template_name = 'main/admin/exam_papers_confirm_delete.html'
    success_url = reverse_lazy('papers_view')
    context_object_name = 'paper'



"""
Subjects
"""

@login_required
@has_to_be_admin
def subjects_view(request):
    subjects = request.user.teaches.all()
    print(subjects, "**********")
    return render(request, 'main/teacher/subjects.html', {'subjects': subjects})