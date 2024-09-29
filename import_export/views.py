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






def export_student_data_to_excel_view(request):
    import openpyxl
    from main.models import Student  # Student Model from main app
    from django.http import HttpResponse


    # Create a new Excel workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Students Data'
    
    # Add headers to the worksheet
    headers = ['Class', 'Roll No', 'Full Name'] 
    ws.append(headers)
    
    # Query the data from the database
    student_data = Student.objects.all().values_list('grade__name', 'grade__section', 'roll_no', 'name')


    #group students by class and section if possible
    temp_dict = {}
    for data in student_data:
        if data[1] != '':
            grade = f"{data[0]} - {data[1]}"
        else:
            grade = data[0]

        if grade not in temp_dict:
            temp_dict[grade] = [(data[2], data[3])]
        else:
            temp_dict[grade].append((data[2], data[3]))
        
    

    # Write student_data to the worksheet
    for key, values in temp_dict.items():
        grade = key
        for roll_no, name in values:
            new_row = (grade, roll_no, name)
            ws.append(new_row)
            # print(new_row)
    
    # Prepare the response as a downloadable Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    import datetime
    response['Content-Disposition'] = f'attachment; filename=students_data-{datetime.datetime.now()}.xlsx'
    
    # Save the workbook to the response
    wb.save(response)
    
    return response
