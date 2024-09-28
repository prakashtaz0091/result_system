from django.shortcuts import render, redirect
from django.contrib import messages

def import_students_view(request):
    from main.models import Student, Grade


    if request.method == 'POST':
        
        excel_file = request.FILES['excel_file']
        # print(excel_file)

        import openpyxl
        from main.models import Student  # Student Model from main app

     
        workbook = openpyxl.load_workbook(excel_file)

        # Select the active worksheet
        sheet = workbook.active

        # Read the data
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping the header row
            # Split the class name and section while handling potential non-string types
            row0 = str(row[0]).strip()
            if isinstance(row0, str) and '-' in row0:
                class_name, section = map(str.strip, row0.split('-'))
            else:
                class_name = str(row0).strip()
                section = ''

            data.append({
                'grade': class_name,
                'section': section,
                'roll_no': row[1],
                'full_name': row[2]
            })


        #group data by class and section if possible
        from itertools import groupby
        data = groupby(data, key=lambda x: (x['grade'], x['section']))


        for key, values in data:
            grade_name, section = key
            
            try:
                if section != '':
                    grade = Grade.objects.get(name=grade_name, section=section)
                else:
                    grade = Grade.objects.get(name=grade_name)
            except Grade.DoesNotExist:
                grade = Grade.objects.create(name=grade_name, section=section, teacher=None)

            print(grade, grade_name)
            for value in values:
                # print(value)
                try:
                    student = Student.objects.get(grade=grade, roll_no=value['roll_no'], name=value['full_name'])
                except Student.DoesNotExist:
                    Student.objects.create(
                        grade=grade,  
                        roll_no=value['roll_no'],
                        name=value['full_name']
                    )

       

        message = "Students imported successfully"
        messages.success(request, message)
        return redirect('import_students_view')
    


    context = {
        'students': Student.objects.all()
    }
    
    return render(request, 'import_export/students.html', context)
