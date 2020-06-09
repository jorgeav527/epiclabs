from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np

from tests_concrete.models import DiamondPiceBreak, DiamondPice
from tests_concrete.forms import DiamondPiceBreakForm, DiamondPiceBreakFormClient, DiamondPiceFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def diamond_pice_break_list(request):
    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = DiamondPiceBreak.objects.filter(user=request.user)
        context = {
            "file_name": "Testigos_Diamantinos",
            "title": "Ensayos de Rotura de Testigos Diamantinos",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = DiamondPiceBreak.objects.all()
        context = {
            "file_name": "Testigos_Diamantinos",
            "title": "Ensayos de Rotura de Testigos Diamantinos",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_list.html', context)        


@login_required
def diamond_pice_break_create(request):
    if request.user.is_bach or request.user.is_group:
        form = DiamondPiceBreakForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Maquina Compresora", "Equipo Perforador"))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:diamond_pice_break_list')
    elif request.user.is_superuser or request.user.is_admin:
        form = DiamondPiceBreakFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Maquina Compresora", "Equipo Perforador"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:diamond_pice_break_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, "tests_concrete/diamond_pice_break/diamond_pice_break_form.html", context)


@login_required
def diamond_pice_break_update(request, id):
    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(DiamondPiceBreak, id=id)
        form = DiamondPiceBreakForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_concrete:diamond_pice_break_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(DiamondPiceBreak, id=id)
        form = DiamondPiceBreakFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_concrete:diamond_pice_break_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, "tests_concrete/diamond_pice_break/diamond_pice_break_form.html", context)


@login_required
def diamond_pice_save(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Regla Graduada",))

    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = DiamondPiceFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    D_passed = instance.D
                    L_passed = instance.L
                    check_per = instance.check_per
                    if L_passed/D_passed > 1.75:
                        messages.error(request, f"El diametro y la longitud no cumplen la norma NTP")
                        return redirect('tests_concrete:diamond_pice_save', id=obj.id)
                    elif check_per == False:
                        messages.error(request, f"El testigo no cumple con la perpendicularidad adecuada")
                        return redirect('tests_concrete:diamond_pice_save', id=obj.id)
                    else:
                        instance.save()
                        for equip in equips:
                            instance.equipment.add(equip)
                            equip.use = F("use") + 1
                            equip.save()
                        messages.success(request, f"Los ensayos han sido creados o actualizados")
                formset.save()
                return redirect('tests_concrete:diamond_pice_save', id=obj.id)
    
    formset = DiamondPiceFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Compresión de Testigos Diamantinos",
    }

    return render(request, "tests_concrete/diamond_pice_break/diamond_pice_form.html", context)


@login_required
def diamond_pice_break_detail(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)

    # Compretion Simple
    qs_diamond_pice = DiamondPice.objects.filter(diamond_pice_break=obj.id)

    context = {
        "obj": obj,
        "qs_diamond_pice": qs_diamond_pice,
        "title": "Detalles del Ensayo de Rotura de Testigos Diamantinos",
        "norma_ASTM": "ASTM C-109",
        "noma_NTP": "NTP 334.034",
    }

    return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_detail.html', context)


@login_required
def diamond_pice_break_delete(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Equipo Perforador"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_concrete:diamond_pice_break_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_delete_comfirm.html', context)


@login_required
def diamond_pice_break_pdf(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first() 

    # Compretion Simple
    qs_diamond_pice = DiamondPice.objects.filter(diamond_pice_break=obj.id)

    context = {
        "obj": obj,
        "qs_diamond_pice": qs_diamond_pice,
        "title": "CONCRETO. MÉTODO DE ENSAYO NORMALIZADO PARA LA DETERMINACIÓN DE LA RESISTENCIA A LA COMPRESIÓN DE TESTIGOS DIAMANTINOS EN MUESTRAS CILINDRICAS.",
        "norma_ASTM": "ASTM C-109",
        "noma_NTP": "NTP 334.034",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_concrete/diamond_pice_break/diamond_pice_break_pdf.html', context)
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
