from django.db import models
from django.contrib.auth.models import User
from .custom_model_fields import NepaliDateField

class Grade(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, default="-")
    teacher = models.OneToOneField(User,verbose_name="Class Teacher", on_delete=models.CASCADE, related_name="class_teacher", null=True)

    class Meta:
        unique_together = ('name', 'section')

    def __str__(self):
        return self.name + " - " + self.section if self.section != "" else self.name
    

    def full_name(self):
        if self.section == "-":
            return self.name
        return f"{self.name} - {self.section}"






class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="students")


    class Meta:
        unique_together = ('name', 'roll_no', 'grade')

    def __str__(self):
        return self.grade.name + " - " + self.grade.section if self.grade.section != '-' else '' + " - " + self.name
    



class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="Subject Name")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="subjects")
    subject_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teaches", null=True)


    class Meta:
        unique_together = ('name', 'grade')

    def __str__(self):
        return f"{self.grade.full_name()}'s {self.name}  ---subject teacher---> {self.subject_teacher.username}"
    




class Exam(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    start_date = NepaliDateField(blank=True, null=True)
    end_date = NepaliDateField(blank=True, null=True)

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return f"{self.name} - {self.year}"
    
    @classmethod
    def get_readable_date(cls,date):
        NEPALI_MONTH_MAPPING = {
            '1':'Baisakh',
            '2':'Jestha',
            '3':'Ashadh',
            '4':'Shrawan',
            '5':'Bhadra',
            '6':'Ashwin',
            '7':'Kartik',
            '8':'Mangsir',
            '9':'Poush',
            '10':'Magh',
            '11':'Falgun',
            '12':'Chaitra'

        }
        year, month_number, day = date.split('-')
        month_number = month_number[1] if month_number[0] == '0' else month_number
        return f"{NEPALI_MONTH_MAPPING[month_number]} {day}, {year}"


    
    @property
    def readable_start_date(self):
        return Exam.get_readable_date(self.start_date)
    

    @property
    def readable_end_date(self):
        return Exam.get_readable_date(self.start_date)



class ExamPaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="papers")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="papers")
    theory_full_marks = models.IntegerField()
    theory_pass_marks = models.IntegerField()
    practical_full_marks = models.IntegerField()
    practical_pass_marks = models.IntegerField()
    marks_entry_done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('exam', 'subject')

    def __str__(self):
        return f"{self.subject.grade.name} - {self.subject.name} - {self.exam.name}"
    

    @property
    def total_full_marks(self):
        return self.theory_full_marks + self.practical_full_marks



class MarksEntry(models.Model):
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE, related_name="marks_entries")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks_entries")
    theory_marks = models.IntegerField(null=True, blank=False)
    practical_marks = models.IntegerField(null=True, blank=False)


    class Meta:
        unique_together = ('exam_paper', 'student')
        verbose_name_plural = "Marks Entries"

    def __str__(self):
        return f"{self.student.name} - {self.exam_paper}"
    

    @property
    def th_plus_pr_marks(self):
        return self.theory_marks + self.practical_marks
    

    # Grade rules and mapping
    grade_mapping = [
        (90, 'A+', 4.0, 'Outstanding'),
        (80, 'A', 3.6, 'Excellent'),
        (70, 'B+', 3.2, 'Very Good'),
        (60, 'B', 2.8, 'Good'),
        (50, 'C+', 2.4, 'Satisfactory'),
        (39, 'C', 2.0, 'Acceptable'),
        (0, 'D', 'NG', 'Insufficient')  # NG for marks below 40
    ]


    @property
    def subject_percentage(self):
        return (self.th_plus_pr_marks / self.exam_paper.total_full_marks) * 100
    

    @property
    def is_pass(self):
        return self.theory_marks >= self.exam_paper.theory_pass_marks and self.practical_marks >= self.exam_paper.practical_pass_marks

    @property
    def marks_grade(self):
        subject_percentage = self.subject_percentage
        if self.is_pass:
            for grade_rule in self.grade_mapping:
                
                if subject_percentage > grade_rule[0]:
                    return grade_rule[1]
        else:
            return self.grade_mapping[6][1]
            
    
    @property
    def marks_grade_point(self):
        subject_percentage = self.subject_percentage
        if self.is_pass:
            for grade_rule in self.grade_mapping:
                
                if subject_percentage > grade_rule[0]:
                    return grade_rule[2]
        else:
            return self.grade_mapping[6][2]
            

    @property
    def marks_grade_remarks(self):
        subject_percentage = self.subject_percentage
        if self.is_pass:
            for grade_rule in self.grade_mapping:
                
                if subject_percentage > grade_rule[0]:
                    return grade_rule[3]
        else:
            return self.grade_mapping[6][3]
        



class ProfileReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="profile_reports")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="profile_reports")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="profile_reports")

    report_choices = [
        ('Outstanding', 'Outstanding'),
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Satisfactory', 'Satisfactory'),
        ('Acceptable', 'Acceptable'),
        ('Insufficient', 'Insufficient'),
    ]

    discipline = models.CharField(max_length=50, choices=report_choices, default="Please edit this field")
    hygiene = models.CharField(max_length=50, choices=report_choices, default="Please edit this field")
    conversation = models.CharField(max_length=50, choices=report_choices, default="Please edit this field")
    reading = models.CharField(max_length=50, choices=report_choices, default="Please edit this field")
    writing = models.CharField(max_length=50, choices=report_choices, default="Please edit this field")
    regularity = models.CharField(max_length=50, choices=report_choices, default="Please edit this field")

    class Meta:
        unique_together = ('student', 'exam', 'grade')
    

    def __str__(self):
        return f"{self.exam} - Grade {self.grade.name} - {self.student.name}"