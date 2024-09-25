from django.forms import ModelForm
from .models import Student, Grade, Subject, Exam, ExamPaper
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import datetime


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'name']
        widgets = {
            'roll_no': forms.TextInput(attrs={'class': 'form-control '}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        student = super(StudentForm, self).save(commit=False)
        student.name = student.name.title()
        if commit:
            student.save()
        return student

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name','section','teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        # Exclude superusers from the teacher field queryset
        self.fields['teacher'].queryset = User.objects.filter(is_superuser=False)

    



class TeacherForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password",
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password",
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Initialize the form
        super(TeacherForm, self).__init__(*args, **kwargs)
        # Make password required if the form is for creating a new user
        if self.instance and self.instance.pk:
            # Update view - set password as not required
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
        else:
            # Create view - set password as required
            self.fields['password'].required = True
            self.fields['confirm_password'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Password and confirm password validation
        if password or confirm_password:  # Check only if either is provided
            if password and confirm_password and password != confirm_password:
                raise ValidationError("Passwords do not match.")

        # Capitalize first name and last name
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name:
            cleaned_data['first_name'] = first_name.capitalize()

        if last_name:
            cleaned_data['last_name'] = last_name.capitalize()

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            # Only hash and set the password if it's provided
            user.password = make_password(password)
        elif not user.pk:
            # Handle case where new user might not have a password
            user.set_unusable_password()

        if commit:
            user.save()
        return user
    



class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'subject_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'subject_teacher': forms.Select(attrs={'class': 'form-control'}),
        }

    
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        # Exclude superusers from the teacher field queryset
        self.fields['subject_teacher'].queryset = User.objects.filter(is_superuser=False)




class ExamForm(forms.ModelForm):
    year = forms.ChoiceField(label="Year", widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Exam
        fields = ['name', 'year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        current_year = datetime.now().year
        start_year = current_year - 1
        end_year = current_year + 10
        
        # Generate a list of choices for the year field
        years = [(year, year) for year in range(start_year, end_year + 1)]
        
        # Set the choices for the year field
        self.fields['year'].choices = years



class ExamPaperForm(forms.ModelForm):

    class Meta:
        model = ExamPaper
        fields = ['exam', 'subject', 'theory_full_marks', 'theory_pass_marks', 'practical_full_marks', 'practical_pass_marks']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'theory_full_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'theory_pass_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'practical_full_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'practical_pass_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }



