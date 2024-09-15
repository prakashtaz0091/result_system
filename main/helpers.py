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