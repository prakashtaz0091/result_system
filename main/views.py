from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .import forms


@login_required
def admin_view(request):
    return render(request, 'main/admin.html')


@login_required
def home(request):
    return render(request, 'main/home.html')









@login_required
def add_students(request):
    """
    view to add students
    """

    if request.method == 'POST':
        form_data = request.POST
        roll_no = form_data['student_roll_no']
        name = form_data['student_name'].title()

        Student.objects.create(roll_no=roll_no, name=name, grade=request.user.class_teacher)
        
        return redirect('add_students')
        


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

    return render(request, 'main/add_students.html', context)



class StudentUpdateView(UpdateView):
    model = Student
    form_class = forms.StudentForm
    template_name = 'main/student_update.html'
    success_url = reverse_lazy('add_students')  # Redirect URL after successful update.


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'main/student_confirm_delete.html'
    success_url = reverse_lazy('add_students')  # Redirect URL after successful deletion.