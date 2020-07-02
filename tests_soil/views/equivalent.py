from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np
import math

from tests_soil.models import Equivalent, Equiv
from tests_soil.forms import EquivalentForm, EquivalentFormClient, EquivFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def equivalent_list(request):
    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = Equivalent.objects.filter(user=request.user)
        context = {
            "file_name": "Determinación_del_Equivalente_de_Arena",
            "title": "Ensayos de la Determinación del Equivalente de Arena",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/equivalent/equivalent_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = Equivalent.objects.all()
        context = {
            "file_name": "Determinación_del_Equivalente_de_Arena",
            "title": "Ensayos de la Determinación del Equivalente de Arena",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/equivalent/equivalent_list.html', context)        


@login_required
def equivalent_create(request):
    if request.user.is_bach or request.user.is_group:
        form = EquivalentForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza"))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:equivalent_list')
    elif request.user.is_superuser or request.user.is_admin:
        form = EquivalentFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:equivalent_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de la Determinación del Equivalente de Arena",
    }

    return render(request, "tests_soil/equivalent/equivalent_form.html", context)


@login_required
def equiv_save(request, id):
    obj = get_object_or_404(Equivalent, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = EquivFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                formset.save()                
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_soil:equiv_save', id=obj.id)
    
    formset = EquivFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de la Determinación del Equivalente de Arena",
    }

    return render(request, "tests_soil/equivalent/equiv_form.html", context)


@login_required
def equivalent_update(request, id):
    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(Equivalent, id=id)
        form = EquivalentForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:equivalent_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(Equivalent, id=id)
        form = EquivalentFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:equivalent_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de la Determinación del Equivalente de Arena",
    }

    return render(request, "tests_soil/equivalent/equivalent_form.html", context)


@login_required
def equivalent_detail(request, id):
    obj = get_object_or_404(Equivalent, id=id)
    qs_equiv = Equiv.objects.filter(equivalent=obj.id)

    # Mean of the equiv sand results
    equiv_sand = qs_equiv.values_list("equiv_sand", flat=True).order_by("id")
    mean_equiv_sand = math.ceil(np.mean(equiv_sand))

    context = {
        "obj": obj,
        "qs_equiv": qs_equiv,
        "mean_equiv_sand": mean_equiv_sand,
        "norma_ASTM": "",
        "noma_NTP": "NTP 339.146",
        "title": "Detalles del Ensayo de la Determinación del Equivalente de Arena",
    }

    return render(request, 'tests_soil/equivalent/equivalent_detail.html', context)


@login_required
def equivalent_delete(request, id):
    obj = get_object_or_404(Equivalent, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:equivalent_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de la Determinación del Equivalente de Arena",
    }

    return render(request, 'tests_soil/equivalent/equivalent_delete_comfirm.html', context)


@login_required
def equivalent_pdf(request, id):
    obj = get_object_or_404(Equivalent, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()
    qs_equiv = Equiv.objects.filter(equivalent=obj.id)

    # Mean of the equiv sand results
    equiv_sand = qs_equiv.values_list("equiv_sand", flat=True).order_by("id")
    mean_equiv_sand = math.ceil(np.mean(equiv_sand))

    context = {
        "obj": obj,
        "qs_equiv": qs_equiv,
        "mean_equiv_sand": mean_equiv_sand,
        "title": "METODO DE ENSAYO ESTÁNDAR PARA EL VALOR EQUIVALENTE DE ARENA DE SUELOS Y AGREGADO FINO - MTC E114",
        "norma_ASTM": "",
        "noma_NTP": "NTP 339.146",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/equivalent/equivalent_pdf.html', context)
    css_bootstrap = CSS(settings.STATIC_ROOT +  '/css/bootstrap.min.css')
    css_pdf = CSS(settings.STATIC_ROOT +  '/css/pdf_file.css')
    filename = f"Ensayo_{obj.user.username}_{obj.id}.pdf"
    response = HttpResponse(content_type="application/pdf")
    # Display in browser
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
    # Download as attachment
    # response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[css_bootstrap, css_pdf])
    return response



