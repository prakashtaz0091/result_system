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
    students_marks = defaultdict(dict)
    
    # Filter MarksEntry by grade
    marks_entries = MarksEntry.objects.filter(
        student__grade=grade  # Filter by student grade
    ).select_related('student', 'exam_paper__subject')
    
    # Loop through each mark entry and build the dictionary
    for entry in marks_entries:
        student_name = entry.student.name
        subject_name = entry.exam_paper.subject.name
        theory_marks = (entry.theory_marks or 0)
        practical_marks = (entry.practical_marks or 0)
        total_marks = theory_marks + practical_marks
        
        # Add subject marks for the student
        students_marks[student_name][subject_name] = {
            'total_marks':{
                'theory_full_marks':entry.exam_paper.theory_full_marks,
                'theory_pass_marks':entry.exam_paper.theory_pass_marks,
                'practical_full_marks':entry.exam_paper.practical_full_marks,
                'practical_pass_marks':entry.exam_paper.practical_pass_marks,

            },
            'obtained_marks':{
                'theory_marks':theory_marks,
                'practical_marks':practical_marks
            }
        }
    
    # Convert defaultdict to a normal dictionary before returning
    return dict(students_marks)