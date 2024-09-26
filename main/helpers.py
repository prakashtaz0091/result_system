def get_paper_student_marks(theory_marks, practical_marks):
    """
    extracts exam_paper, student, marks data from form_data
    """

    key1, value1 = theory_marks
    key2, value2 = practical_marks
    
    exam_paper_id1 = key1.split('_')[0]
    student_id1 = key1.split('_')[1]

    exam_paper_id2 = key1.split('_')[0]
    student_id2 = key1.split('_')[1]


    if exam_paper_id1 != exam_paper_id2 or student_id1 != student_id2:
        raise ValueError('There is some error while submitting the marks')
    

    theory_marks = value1
    practical_marks = value2
    return exam_paper_id1, student_id1, theory_marks, practical_marks





#for getting marks for report card
from collections import defaultdict
from .models import MarksEntry

def get_students_marks_for_grade(grade):
    # Create a dictionary to store student marks
    temp_dict = defaultdict(dict)
    
    # Filter MarksEntry by grade
    marks_entries = MarksEntry.objects.filter(
        student__grade=grade  # Filter by student grade
    ).select_related('student', 'exam_paper__subject')
    
    # Loop through each mark entry and build the dictionary
    for entry in marks_entries:
        student_name = entry.student.name.lower()  # Making student name lowercase
        subject_name = entry.exam_paper.subject.name
        theory_marks = (entry.theory_marks or 0)
        practical_marks = (entry.practical_marks or 0)

        # Initialize student object and marks dictionary
        if 'student_object' not in temp_dict[student_name]:
            temp_dict[student_name]['student_object'] = entry.student
            temp_dict[student_name]['marks'] = {}  # Add the 'marks' key

        # Add subject marks under the 'marks' key
        temp_dict[student_name]['marks'][subject_name] = {
            'total_marks': {
                'theory_full_marks': entry.exam_paper.theory_full_marks,
                'theory_pass_marks': entry.exam_paper.theory_pass_marks,
                'practical_full_marks': entry.exam_paper.practical_full_marks,
                'practical_pass_marks': entry.exam_paper.practical_pass_marks,
            },
            'obtained_marks': {
                'theory_marks': theory_marks,
                'practical_marks': practical_marks
            }
        }
    
    # Convert defaultdict to a normal dictionary before returning
    return dict(temp_dict)




    





# Grade rules and mapping
GRADE_MAPPING = [
    (90, 'A+', 4.0, 'Outstanding'),
    (80, 'A', 3.6, 'Excellent'),
    (70, 'B+', 3.2, 'Very Good'),
    (60, 'B', 2.8, 'Good'),
    (50, 'C+', 2.4, 'Satisfactory'),
    (39, 'C', 2.0, 'Acceptable'),
    (0, 'D', 'NG', 'Insufficient')  # NG for marks below 40
]


def get_grade(percentage):
    for grade_rule in GRADE_MAPPING:
            if percentage > grade_rule[0]:
                return grade_rule[1]


def get_grade_point(percentage):
    for grade_rule in GRADE_MAPPING:
        if percentage > grade_rule[0]:
            return grade_rule[2]
        


def get_remarks(percentage):
    for grade_rule in GRADE_MAPPING:
        if percentage > grade_rule[0]:
            return grade_rule[3]



FINAL_REMARKS = [
    (90, 'Outstanding Keep it up.'),
    (80, 'Excellent keep it up.'),
    (70, 'Very Good labor more.'),
    (60, 'Good hard labor will prove better result.'),
    (50, 'Labor hard for better result.'),
    (39, 'Labor hard for better result.'),
    (0, 'Very Poor, avoid negligence')  # NG for marks below 40
]

def get_final_remarks(percentage):
    for remarks in FINAL_REMARKS:
        if percentage > remarks[0]:
            return remarks[1]



def add_grand_total(temp_dict):

    for student_name,student_related_data in temp_dict.items():
        if 'grand_total' not in student_related_data.keys():
            student_related_data['grand_total'] = {
                'theory_full_marks': 0,
                'practical_full_marks': 0,
                'theory_pass_marks': 0,
                'practical_pass_marks': 0,
                'total_marks': 0,
                'obtained_marks': 0,
                'final_grade': '',
                'final_grade_point': 0.0,
                'remarks': '',
                'percentage': 0.0,
                'rank': '',
                'fail': False,
            }
            
        for subject_name, subject_data in student_related_data['marks'].items():
            student_related_data['grand_total']['theory_full_marks'] += subject_data['total_marks']['theory']['full']
            student_related_data['grand_total']['practical_full_marks'] += subject_data['total_marks']['practical']['full']
            student_related_data['grand_total']['theory_pass_marks'] += subject_data['total_marks']['theory']['pass']
            student_related_data['grand_total']['practical_pass_marks'] += subject_data['total_marks']['practical']['pass']
            student_related_data['grand_total']['total_marks'] += subject_data['total_marks']['theory']['full'] + subject_data['total_marks']['practical']['full']
            student_related_data['grand_total']['obtained_marks'] += subject_data['obtained_marks']['theory_marks'] + subject_data['obtained_marks']['practical_marks']

            #check if pass or fail
            if subject_data['obtained_marks']['theory_marks'] < subject_data['total_marks']['theory']['pass'] or subject_data['obtained_marks']['practical_marks'] < subject_data['total_marks']['practical']['pass']:  
                student_related_data['grand_total']['fail'] = True

    return temp_dict



def add_final_calculations(temp_dict):
    for student_name, student_data in temp_dict.items():
        total_percentage = (student_data['grand_total']['obtained_marks']/student_data['grand_total']['total_marks'])*100
        student_data['grand_total']['percentage'] = round(total_percentage,1)
        student_data['grand_total']['final_grade'] = get_grade(total_percentage)
        student_data['grand_total']['final_grade_point'] = get_grade_point(total_percentage)

        if not student_data['grand_total']['fail']:
            student_data['grand_total']['remarks'] = get_final_remarks(total_percentage)
        else:
            student_data['grand_total']['remarks'] = FINAL_REMARKS[-1][1]

        
    return temp_dict


# def calculate_ranks(students_data):
#     # Step 1: Create a list of tuples (student_name, obtained_marks) from the data
#     student_marks_list = [(student_name, data['grand_total']['obtained_marks']) 
#                           for student_name, data in students_data.items()]

#     # Step 2: Sort the students based on obtained_marks in descending order
#     sorted_students = sorted(student_marks_list, key=lambda x: x[1], reverse=True)

#     # Step 3: Assign ranks
#     rank = 1
#     for index, (student_name, obtained_marks) in enumerate(sorted_students):
#         # If current student has the same marks as the previous one, assign the same rank
#         if index > 0 and obtained_marks == sorted_students[index - 1][1]:
#             students_data[student_name]['grand_total']['rank'] = students_data[sorted_students[index - 1][0]]['grand_total']['rank']
#         else:
#             students_data[student_name]['grand_total']['rank'] = rank
        
#         # Increment rank for the next student
#         rank += 1

#     return students_data


def calculate_ranks(students_data):
    # Step 1: Create a list of tuples (student_name, obtained_marks) from the data
    # but only include students who have not failed (fail == False)
    student_marks_list = [
        (student_name, data['grand_total']['obtained_marks']) 
        for student_name, data in students_data.items()
        if not data['grand_total'].get('fail', False)  # Skip if 'fail' is True
    ]

    # Step 2: Sort the students based on obtained_marks in descending order
    sorted_students = sorted(student_marks_list, key=lambda x: x[1], reverse=True)

    # Step 3: Assign ranks
    rank = 1
    for index, (student_name, obtained_marks) in enumerate(sorted_students):
        # If the current student has the same marks as the previous one, assign the same rank
        if index > 0 and obtained_marks == sorted_students[index - 1][1]:
            students_data[student_name]['grand_total']['rank'] = students_data[sorted_students[index - 1][0]]['grand_total']['rank']
        else:
            students_data[student_name]['grand_total']['rank'] = rank
        
        # Increment rank for the next student
        rank += 1

    # Optional: Set rank as None or 'N/A' for failed students
    for student_name, data in students_data.items():
        if data['grand_total'].get('fail', False):
            students_data[student_name]['grand_total']['rank'] = 'N/A'  # You can set this to whatever is appropriate

    return students_data




from .models import ProfileReport
def get_profile_report(student, exam):
    profile_report = ProfileReport.objects.filter(student=student, exam=exam, grade = student.grade)

    if not profile_report.exists():
        return None
    
    return profile_report.first()


def get_reports(grade, exam):
    # Create a dictionary to store student marks
    temp_dict = defaultdict(dict)
    
    # Filter MarksEntry by grade
    marks_entries = MarksEntry.objects.filter(
        student__grade=grade,
        exam_paper__exam=exam  # Filter by student grade
    ).select_related('student', 'exam_paper__subject')
    
    # Loop through each mark entry and build the dictionary
    for entry in marks_entries:
        student_name = entry.student.name.lower()  # Making student name lowercase
        student = entry.student
        subject_name = entry.exam_paper.subject.name
        obtained_th_marks = (entry.theory_marks or 0)
        obtained_pr_marks = (entry.practical_marks or 0)
        total_obtained_marks = entry.th_plus_pr_marks

        # Ensure 'marks' key exists for the student
        if 'marks' not in temp_dict[student_name]:
            temp_dict[student_name]['marks'] = {}

        # Assign subject marks data
        temp_dict[student_name]['marks'][subject_name] = {
            'total_marks': {
                'theory':{
                    'full': entry.exam_paper.theory_full_marks,
                    'pass': entry.exam_paper.theory_pass_marks
                },
                'practical':{
                    'full': entry.exam_paper.practical_full_marks,
                    'pass': entry.exam_paper.practical_pass_marks
                },
                'total': entry.exam_paper.total_full_marks
            },
            'obtained_marks':{
                'theory_marks': obtained_th_marks,
                'practical_marks': obtained_pr_marks,
                'total_marks_obtained': total_obtained_marks,
                'subject_grade': entry.marks_grade,
                'subject_grade_point': entry.marks_grade_point,
                'subject_remarks': entry.marks_grade_remarks
            },
            
        }

        temp_dict[student_name]['student_obj'] = student
        temp_dict[student_name]['profile_report'] = get_profile_report(student, exam)


    temp_dict = add_grand_total(temp_dict)
    temp_dict = add_final_calculations(temp_dict)
    temp_dict = calculate_ranks(temp_dict)

    return temp_dict
    

