from django.db import models
from django.contrib.auth.models import User


class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True)
    teacher = models.OneToOneField(User,verbose_name="Class Teacher", on_delete=models.CASCADE, related_name="class_teacher")


    def __str__(self):
        return self.name






class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField(unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.name
    



class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="Subject Name")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="subjects")
    subject_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teaches")


    class Meta:
        unique_together = ('name', 'grade')

    def __str__(self):
        return f"{self.name} ---of---> {self.grade.name} ---is taught by---> {self.subject_teacher.username}"
    




class Exam(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return f"{self.name} - {self.year}"