from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ConstructionForm
from .models import Construction 

# Create your views here.

@login_required
def construction_create(request):
    if request.user.is_client:
        form = ConstructionForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.instance.client_profile = request.user.clientprofile
                form.save()
                messages.success(request, f"La Construcción a sido Creada")
                return redirect('accounts:profile_client')
    
    else:
        form = ConstructionForm(instance=request.user.clientprofile)

    context = {
        "form": form,
        "title": "Crear Construcción",
    }

    return render(request, "construction/construction_form.html", context)


@login_required
def construction_update(request, id):
    obj = get_object_or_404(Construction, id=id)
    form = ConstructionForm(request.POST or None, instance=obj)
    if request.user.is_client:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"La construcción a sido Actualizada")
                return redirect('accounts:profile_client')
    
    else:
        form = ConstructionForm(request.POST or None, instance=obj)

    context = {
        "obj": obj,
        "form": form,
        "title": "Actualizar Construcción",
    }

    return render(request, "construction/construction_form.html", context)


@login_required
def construction_delete(request, id):
    obj = get_object_or_404(Construction, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"La construcción a sido eliminada")
        return redirect('accounts:profile_client')

    context = {
        "obj": obj,
        "title": "Eliminar la Construction:",
    }

    return render(request, 'construction/construction_delete_comfirm.html', context)


def load_construction(request):
    user_id = request.GET.get('user')
    construction = Construction.objects.filter(client_profile__user=user_id)

    context ={
        "construction": construction,
    }

    return render(request, 'construction/construction_dropdown_list_options.html', context)