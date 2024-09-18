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





# def students_marks_describe(student_wise_subject_marks):
#     # Grade rules and mapping
#     grade_mapping = [
#         (90, 'A+', 4.0, 'Outstanding'),
#         (80, 'A', 3.6, 'Excellent'),
#         (70, 'B+', 3.2, 'Very Good'),
#         (60, 'B', 2.8, 'Good'),
#         (50, 'C+', 2.4, 'Satisfactory'),
#         (40, 'C', 2.0, 'Acceptable'),
#         (0, 'D', 0.0, 'Insufficient')  # NG for marks below 40
#     ]
    
#     def get_grade(percentage):
#         for threshold, grade, points, remarks in grade_mapping:
#             if percentage >= threshold:
#                 return grade, points, remarks
#         return 'D', 0.0, 'Insufficient'  # Default for marks < 40
    
#     # Loop through each student
#     for student_name, student_data in student_wise_subject_marks.items():
#         total_obtained_marks = 0
#         total_full_marks = 0
#         total_grade_points = 0
#         subject_count = 0
        
#         # Process each subject for the student
#         for subject, subject_data in student_data['marks'].items():
#             theory_marks = subject_data['obtained_marks']['theory_marks']
#             practical_marks = subject_data['obtained_marks']['practical_marks']
            
#             # Calculate total obtained marks for the subject
#             total_subject_marks = theory_marks + practical_marks
#             subject_data['obtained_marks']['total_marks_obtained'] = total_subject_marks
            
#             # Calculate the full marks for the subject
#             theory_full_marks = subject_data['total_marks']['theory_full_marks']
#             practical_full_marks = subject_data['total_marks']['practical_full_marks']
#             full_subject_marks = theory_full_marks + practical_full_marks
            
#             # Calculate percentage for the subject
#             percentage = (total_subject_marks / full_subject_marks) * 100
            
#             # Get final grade and grade points based on percentage
#             final_grade, grade_points, remarks = get_grade(percentage)
#             subject_data['obtained_marks']['final_grade'] = final_grade
#             subject_data['obtained_marks']['grade_points'] = grade_points
#             subject_data['obtained_marks']['remarks'] = remarks
            
#             # Accumulate the totals
#             total_obtained_marks += total_subject_marks
#             total_full_marks += full_subject_marks
#             total_grade_points += grade_points
#             subject_count += 1
        
#         # Calculate overall percentage and GPA for the student
#         total_percentage = (total_obtained_marks / total_full_marks) * 100 if total_full_marks > 0 else 0
#         gpa = total_grade_points / subject_count if subject_count > 0 else 0
        
#         # Append total percentage, GPA, and grade points to the student data
#         student_data['total_percentage'] = total_percentage
#         student_data['gpa'] = gpa
#         student_data['total_grade_points'] = total_grade_points
    
#     # Return the updated dictionary
#     return student_wise_subject_marks




def students_marks_describe(student_wise_subject_marks):
    # Grade rules and mapping
    grade_mapping = [
        (90, 'A+', 4.0, 'Outstanding'),
        (80, 'A', 3.6, 'Excellent'),
        (70, 'B+', 3.2, 'Very Good'),
        (60, 'B', 2.8, 'Good'),
        (50, 'C+', 2.4, 'Satisfactory'),
        (40, 'C', 2.0, 'Acceptable'),
        (0, 'D', 0.0, 'Insufficient')  # NG for marks below 40
    ]
    
    def get_grade(percentage):
        for threshold, grade, points, remarks in grade_mapping:
            if percentage >= threshold:
                return grade, points, remarks
        return 'D', 0.0, 'Insufficient'  # Default for marks < 40
    
    # Loop through each student
    for student_name, student_data in student_wise_subject_marks.items():
        total_obtained_marks = 0
        total_full_marks = 0
        total_grade_points = 0
        subject_count = 0
        
        # Process each subject for the student
        for subject, subject_data in student_data['marks'].items():
            theory_marks = subject_data['obtained_marks']['theory_marks']
            practical_marks = subject_data['obtained_marks']['practical_marks']
            
            # Calculate total obtained marks for the subject
            total_subject_marks = theory_marks + practical_marks
            subject_data['obtained_marks']['total_marks_obtained'] = total_subject_marks  # This is still subject-wise
            
            # Calculate the full marks for the subject
            theory_full_marks = subject_data['total_marks']['theory_full_marks']
            practical_full_marks = subject_data['total_marks']['practical_full_marks']
            full_subject_marks = theory_full_marks + practical_full_marks
            
            # Calculate percentage for the subject
            percentage = (total_subject_marks / full_subject_marks) * 100
            
            # Get final grade and grade points based on percentage
            final_grade, grade_points, remarks = get_grade(percentage)
            subject_data['obtained_marks']['final_grade'] = final_grade
            subject_data['obtained_marks']['grade_points'] = grade_points
            subject_data['obtained_marks']['remarks'] = remarks
            
            # Accumulate the totals for overall marks and grades
            total_obtained_marks += total_subject_marks
            total_full_marks += full_subject_marks
            total_grade_points += grade_points
            subject_count += 1
        
        # Calculate overall percentage and GPA for the student
        total_percentage = (total_obtained_marks / total_full_marks) * 100 if total_full_marks > 0 else 0
        gpa = total_grade_points / subject_count if subject_count > 0 else 0
        
        # Append total obtained marks, total percentage, GPA, and grade points to the student data
        student_data['total_obtained_marks'] = total_obtained_marks
        student_data['total_percentage'] = total_percentage
        student_data['gpa'] = gpa
        student_data['total_grade_points'] = total_grade_points
        student_data['final_grade'] = get_grade(total_percentage)[0]
        student_data['final_remarks'] = get_grade(total_percentage)[2]
    
    # Return the updated dictionary
    return student_wise_subject_marks
