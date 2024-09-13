from django.db import models
from django.contrib.auth.models import User


class Grade(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name="class_teacher")


    def __str__(self):
        return self.name + " - " + self.teacher.username






class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField(unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.name