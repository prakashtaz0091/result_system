from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Grade, Subject, Exam, ExamPaper, MarksEntry
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from .import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .helpers import get_paper_student_marks




@login_required
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
def subjects_view(request):
    exam_papers = ExamPaper.objects.filter(subject__subject_teacher=request.user)
    return render(request, 'main/teacher/subjects.html', {'exam_papers': exam_papers})


"""
marks entry
"""
@login_required
def marks_entry(request, pk):


    #handle marks entry
    if request.method == 'POST':
        form_data = request.POST
        # print(form_data)
        form_data_list = (list(form_data.items())[1:])
        for index in range(0,len(form_data_list), 2):
            """
            form_data_list[index] -> theory marks of a student
            form_data_list[index+1] -> practical marks of a student
            """

            try:
                exam_paper_id, student_id, theory_marks, practical_marks = get_paper_student_marks(form_data_list[index], form_data_list[index+1])
            except ValueError:
                message = "There is some error while submitting the marks"
                messages.warning(request, message)
                return redirect('teachers_subjects_view')
            

            MarksEntry.objects.create(
                exam_paper = get_object_or_404(ExamPaper, pk=exam_paper_id),
                student = get_object_or_404(Student, pk=student_id),
                theory_marks = theory_marks,
                practical_marks = practical_marks
            )

        message = "Marks entered successfully. Thank you"
        messages.success(request, message)
        return redirect('teachers_subjects_view')



    exam_paper = get_object_or_404(ExamPaper, pk=pk)

    #check if marks_entry already done, if done, then redirect to marks entry update page
    if exam_paper.marks_entries.exists():
        message = "You have already done marks entry for this exam paper. Below are the marks obtained by students."
        messages.success(request, message)
        return redirect(reverse('marks_entry_update_view', args=[pk]))

    #show marks entry form
    if exam_paper.subject.subject_teacher != request.user:
        message = "You are only allowed to enter marks for your own subjects"
        messages.warning(request, message)
        return redirect('teachers_subjects_view')
    
    students = exam_paper.subject.grade.students.all()

    

    context = {
        'exam_paper': exam_paper,
        'students': students
    }

    return render(request, 'main/teacher/marks_entry.html', context)




#marks entry update view
@login_required
def marks_entry_update(request, pk):
    
    return render(request, 'main/teacher/marks_entry_update.html', {})