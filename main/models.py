from django.db import models
from django.contrib.auth.models import User


class Grade(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, default="-")
    teacher = models.OneToOneField(User,verbose_name="Class Teacher", on_delete=models.CASCADE, related_name="class_teacher")

    class Meta:
        unique_together = ('name', 'section')

    def __str__(self):
        return self.name + " - " + self.section if self.section != "-" else self.name
    

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
        return self.name
    



class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="Subject Name")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="subjects")
    subject_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teaches")


    class Meta:
        unique_together = ('name', 'grade')

    def __str__(self):
        return f"{self.grade.full_name()}'s {self.name}  ---subject teacher---> {self.subject_teacher.username}"
    




class Exam(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return f"{self.name} - {self.year}"
    



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