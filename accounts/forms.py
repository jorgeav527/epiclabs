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
from course.models import Course
from category.models import Category

# For all the users the same user update form
class AccountUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombres',) 
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos',)
    email = forms.EmailField(max_length=30, required=True, help_text='Solo @gmail',)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

# STUDENT
#========

class StudentRegister(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Solo @gmail',)

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
    dni = forms.IntegerField(required=True, label='DNI', help_text='Documento Nacional de Identidad',)
    codigo = forms.IntegerField(required=True, label='Codigo de Matricula', help_text='2008702131',)

    class Meta:
        model = StudentProfile
        fields = ("dni", "codigo",)


# BACH
#=====

class BachRegister(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Solo @gmail',)

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
    dni         = forms.IntegerField(required=True, label='DNI', help_text='Documento Nacional de Identidad',)
    codigo      = forms.IntegerField(required=True, label='Codigo de Matricula', help_text='2008702131',)

    class Meta:
        model   = BachProfile
        fields  = ("dni", "codigo")

# TEACHER
#========

class TeacherRegister(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Solo @gmail',)

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
    dni         = forms.IntegerField(required=True, label='DNI', help_text='Documento Nacional de Identidad',)
    codigo      = forms.IntegerField(required=True, label='Codigo de Colegiatura',)
    course      = forms.ModelMultipleChoiceField(queryset=Course.objects.all() ,required=True, label='Cursos Impartidos', help_text='Selecciona todas las materias que imparte.',)

    class Meta:
        model   = TeacherProfile
        fields  = ("dni", "codigo", "course")


# CLIENT
#========

class ClientRegister(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Solo @gmail',)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def save(self, commit=True):
        client = super().save(commit=False)
        client.is_client = True
        if commit:
            client.save()
        return client


class ClientAccountUpdatedForm(forms.ModelForm):
    email = forms.EmailField(max_length=30, required=True, help_text='Solo @gmail',)

    class Meta:
        model = User
        fields = ("username", "email",)
        # exclude = ("first_name", "last_name",)


class ClientUpdateForm(forms.ModelForm):
    long_name   = forms.CharField(required=True, label='Nombre de la Empresa',)
    direction   = forms.CharField(required=True, label='Dirección de la Empresa',)
    reference   = forms.CharField(required=True, label='Referencia de la Dirección',)
    category    = forms.ModelMultipleChoiceField(queryset=Category.objects.all() ,required=True, label='Categoria', help_text='Selecciona la Categoria',)
    ruc         = forms.IntegerField(required=True, label='Registro Único de Contribuyentes',)
    phone       = forms.IntegerField(required=True, label='Telefono o Celular',)

    class Meta:
        model   = ClientProfile
        fields  = ("long_name", "direction", "reference", "category", "ruc", "phone",)


# ADMIN
#========

class AdminRegister(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Solo @gmail',)

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
    STAFF_CHOICES = (
        ("NN", "Ninguna"),
        ("OT", "Oficina Técnica"),
        ("S", "Secretaria"),
        ("C", "Coordinador"),
    )
    dni         = forms.IntegerField(required=True, label='DNI', help_text='Documento Nacional de Identidad',)
    codigo      = forms.IntegerField(required=True, label='Codigo de Colegiatura',)
    staff       = forms.ChoiceField(required=True, choices=STAFF_CHOICES, label='Personal de', help_text='Selecciona la labor',)

    class Meta:
        model   = AdminProfile
        fields  = ("dni", "codigo", "staff",)