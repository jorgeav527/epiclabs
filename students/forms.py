from django import forms
from django.forms import inlineformset_factory

from accounts.models import GroupProfile
from .models import StudentGroup

class StudentGroupForm(forms.ModelForm):

    class Meta:
        model = StudentGroup
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

StudentGroupFormSet = inlineformset_factory(GroupProfile, StudentGroup, form=StudentGroupForm, extra=6, max_num=6, can_delete=True)
