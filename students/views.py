from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import StudentGroupFormSet
from accounts.models import GroupProfile

@login_required
def student_group_save(request, id):
    obj = get_object_or_404(GroupProfile, id=id)

    if request.user.is_group:
        if request.method == "POST":
            formset = StudentGroupFormSet(request.POST, instance=obj)
            if formset.is_valid():
                formset.save()                
                messages.success(request, f"Los alumnos han sido creados")
                return redirect('students:student_group_save', id=obj.id)
    
    formset = StudentGroupFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Alumnos",
    }

    return render(request, "students/student_group_form.html", context)