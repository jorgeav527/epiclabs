from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User,
    StudentProfile,
    BachProfile,
    TeacherProfile,
    ClientProfile,
    AdminProfile,
)

# For all the users the same user update form
class AccountUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True) 
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

# STUDENT
#========

class StudentRegister(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'gmail or outlook!',
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def save(self, commit=True):
        student = super().save(commit=False)
        student.is_student = True
        if commit:
            student.save()
        return student


class StudentUpdateForm(forms.ModelForm):
    dni = forms.IntegerField(required=True)
    codigo = forms.IntegerField(required=True)

    class Meta:
        model = StudentProfile
        fields = ("dni", "codigo",)


# BACH
#=====

class BachRegister(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'gmail or outlook!',
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def save(self, commit=True):
        bach = super().save(commit=False)
        bach.is_bach = True
        if commit:
            bach.save()
        return bach


class BachUpdateForm(forms.ModelForm):
    dni         = forms.IntegerField(required=True)
    codigo      = forms.IntegerField(required=True)
    thesis_name = forms.CharField(required=True)

    class Meta:
        model   = BachProfile
        fields  = ("dni", "codigo")

# TEACHER
#========

class TeacherRegister(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'gmail or outlook!',
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.is_teacher = True
        if commit:
            teacher.save()
        return teacher


class TeacherUpdateForm(forms.ModelForm):
    dni         = forms.IntegerField(required=True)
    codigo      = forms.IntegerField(required=True)
    course = forms.CharField(required=True)

    class Meta:
        model   = TeacherProfile
        fields  = ("dni", "codigo", "course")


# CLIENT
#========

class ClientRegister(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'gmail or outlook!',
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def save(self, commit=True):
        client = super().save(commit=False)
        client.is_client = True
        if commit:
            client.save()
        return client


class ClientUpdateForm(forms.ModelForm):
    long_name   = forms.CharField(required=True)
    direction   = forms.CharField(required=True)
    reference   = forms.CharField(required=False)

    class Meta:
        model   = ClientProfile
        fields  = ("long_name", "direction", "reference", "category", "ruc", "phone",)


# ADMIN
#========

class AdminRegister(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'gmail or outlook!',
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.is_admin = True
        if commit:
            admin.save()
        return admin


class AdminUpdateForm(forms.ModelForm):
    dni         = forms.IntegerField(required=True)
    codigo      = forms.IntegerField(required=True)
    course = forms.CharField(required=True)

    class Meta:
        model   = AdminProfile
        fields  = ("dni", "codigo", "staff",)