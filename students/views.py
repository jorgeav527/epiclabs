from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import StudentForm
from .models import Student

@login_required
def student_create(request):
    if request.user.is_group:
        form = StudentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.instance.group_profile = request.user.groupprofile
                form.save()
                messages.success(request, f"El Estudiante a sido Creado")
                return redirect('accounts:profile_group')
    
    else:
        form = StudentForm(instance=request.user.groupprofile)

    context = {
        "form": form,
        "title": "Crear Estudiante",
    }

    return render(request, "student/student_form.html", context)

@login_required
def student_update(request, id):
    obj = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=obj)
    if request.user.is_group:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El Estudiante a sido Actualizado")
                return redirect('accounts:profile_group')
    
    else:
        form = StudentForm(request.POST or None, instance=obj)

    context = {
        "obj": obj,
        "form": form,
        "title": "Actualizar Estudiante",
    }

    return render(request, "student/student_form.html", context)


@login_required
def student_delete(request, id):
    obj = get_object_or_404(Student, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"La Estudiante a sido eliminado")
        return redirect('accounts:profile_group')

    context = {
        "obj": obj,
        "title": "Eliminar el Estudiante",
    }

    return render(request, 'student/student_delete_comfirm.html', context)