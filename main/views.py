from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student


@login_required
def admin_view(request):
    return render(request, 'main/admin.html')


@login_required
def home(request):
    return render(request, 'main/home.html')



def add_students(request):

    if request.method == 'POST':
        form_data = request.POST
        roll_no = form_data['student_roll_no']
        name = form_data['student_name']

        Student.objects.create(roll_no=roll_no, name=name, grade=request.user.class_teacher)
        
        return redirect('add_students')
        


    class_name = request.user.class_teacher

    if class_name is not None:
        students = Student.objects.filter(grade=class_name)
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