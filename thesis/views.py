from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import ThesisForm
from .models import Thesis

# Create your views here.
@login_required
def thesis_create(request):
    if request.user.is_bach:
        form = ThesisForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.instance.bach_profile = request.user.bachprofile
                form.save()
                messages.success(request, f"La Thesis a sido Creada")
                return redirect('accounts:profile_bach')
    
    else:
        form = ThesisForm(instance=request.user.bachprofile)

    context = {
        "form": form,
        "title": "Crear Tesis",
    }

    return render(request, "thesis/thesis_form.html", context)


@login_required
def thesis_update(request, id):
    obj = get_object_or_404(Thesis, id=id)
    form = ThesisForm(request.POST or None, instance=obj)
    if request.user.is_bach:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"La Thesis a sido Actualizada")
                return redirect('accounts:profile_bach')
    
    else:
        form = ThesisForm(request.POST or None, instance=obj)

    context = {
        "obj": obj,
        "form": form,
        "title": "Actualizar Tesis",
    }

    return render(request, "thesis/thesis_form.html", context)


@login_required
def thesis_delete(request, id):
    obj = get_object_or_404(Thesis, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"La tesis a sido eliminada")
        return redirect('accounts:profile_bach')

    context = {
        "obj": obj,
        "title": "Eliminar la Tesis:",
    }

    return render(request, 'thesis/thesis_delete_comfirm.html', context)


