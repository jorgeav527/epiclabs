from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ReferencePersonForm
from .models import ReferencePerson

@login_required
def reference_person_create(request):
    if request.user.is_client:
        form = ReferencePersonForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.instance.client_profile = request.user.clientprofile
                form.save()
                messages.success(request, f"La Persona de Referencia a sido Creada")
                return redirect('accounts:profile_client')
    
    else:
        form = ReferencePersonForm(instance=request.user.clientprofile)

    context = {
        "form": form,
        "title": "Crear Persona de Referencia",
    }

    return render(request, "reference_person/reference_person_form.html", context)

@login_required
def reference_person_update(request, id):
    obj = get_object_or_404(ReferencePerson, id=id)
    form = ReferencePersonForm(request.POST or None, instance=obj)
    if request.user.is_client:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"La Persona de Referencia a sido Actualizada")
                return redirect('accounts:profile_client')
    
    else:
        form = ReferencePersonForm(request.POST or None, instance=obj)

    context = {
        "obj": obj,
        "form": form,
        "title": "Actualizar Persona de Referencia",
    }

    return render(request, "reference_person/reference_person_form.html", context)


@login_required
def reference_person_delete(request, id):
    obj = get_object_or_404(ReferencePerson, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"La Persona de Referencia a sido eliminada")
        return redirect('accounts:profile_client')

    context = {
        "obj": obj,
        "title": "Eliminar la Persona de Referencia",
    }

    return render(request, 'reference_person/reference_person_delete_comfirm.html', context)


def load_reference_person(request):
    user_id = request.GET.get('user')
    reference_person = ReferencePerson.objects.filter(client_profile__user=user_id)

    context ={
        "reference_person": reference_person,
    }

    return render(request, 'reference_person/reference_person_dropdown_list_options.html', context)