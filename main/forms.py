from django.forms import ModelForm
from .models import Student
from django import forms



class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'name']
        widgets = {
            'roll_no': forms.TextInput(attrs={'class': 'form-control '}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }