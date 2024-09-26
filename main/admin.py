from django.contrib import admin

from .models import Grade, Student, Subject, Exam, ExamPaper, MarksEntry, ProfileReport


admin.site.register(Grade)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(ExamPaper)
admin.site.register(MarksEntry)
admin.site.register(ProfileReport)
