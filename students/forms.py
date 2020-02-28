from django import forms
from django.forms import inlineformset_factory

from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "full_name", 
            "codigo", 
            "email", 
            "phone",
        ]
        labels = {
            "full_name": "Nombre Completo", 
            "codigo": "Codigo de Matricula", 
            "email": "Email", 
            "phone": "Telefono o Celular",
        }
        help_texts = {
            "codigo": "2008702131", 
            "email": "Solo @gmail", 
        }

