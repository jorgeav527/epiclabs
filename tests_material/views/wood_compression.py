from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np

from tests_material.models import WoodCompression, ParallelPerpendicular
from tests_material.forms import WoodCompressionForm, WoodCompressionFormClient, ParallelPerpendicularFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

@login_required
def wood_compression_list(request):

    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = WoodCompression.objects.filter(user=request.user)
        context = {
            "file_name": "Compresion_Madera_Paralela_Perpendicular",
            "title": "Ensayos de Compresión Simple Perpendicular o Paralela en Madera",
            "obj_list": obj_list,
        }
        return render(request, 'tests_material/wood_compression/wood_compression_list.html', context)        

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = WoodCompression.objects.all()
        context = {
            "file_name": "Compresion_Madera_Paralela_Perpendicular",
            "title": "Ensayos de Compresión Simple Perpendicular o Paralela en Madera",
            "obj_list": obj_list,
        }
        return render(request, 'tests_material/wood_compression/wood_compression_list.html', context)        


@login_required
def wood_compression_create(request):

    if request.user.is_bach or request.user.is_group:
        form = WoodCompressionForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Maquinas Varias",))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_material:wood_compression_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = WoodCompressionFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Maquinas Varias",))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_material:wood_compression_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Compresión Simple Perpendicular o Paralela en Madera",
    }

    return render(request, "tests_material/wood_compression/wood_compression_form.html", context)


@login_required
def parallel_perpendicular_save(request, id):
    obj = get_object_or_404(WoodCompression, id=id)
    equips = Equip.objects.filter(name__in=("Balanza", "Maquina Compresora", "Regla Graduada",))

    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = ParallelPerpendicularFormSet(request.POST, instance=obj)
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
                return redirect('tests_material:parallel_perpendicular_save', id=obj.id)
    
    formset = ParallelPerpendicularFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación de Variación de Dimenciones",
    }

    return render(request, "tests_material/wood_compression/parallel_perpendicular_form.html", context)


@login_required
def wood_compression_update(request, id):

    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(WoodCompression, id=id)
        form = WoodCompressionForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_material:wood_compression_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(WoodCompression, id=id)
        form = BrickTypeFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_material:wood_compression_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Compresión Simple Perpendicular o Paralela en Madera",
    }

    return render(request, "tests_material/wood_compression/wood_compression_form.html", context)


@login_required
def wood_compression_detail(request, id):
    obj = get_object_or_404(WoodCompression, id=id)

    # Compretion Simple
    qs_parallel_perpendicular = ParallelPerpendicular.objects.filter(wood_compression=obj.id)

    # Parallel
    qs_parallel = qs_parallel_perpendicular.filter(type_compression="PARALELO")
    qs_fc_parallel_list = qs_parallel.values_list('fc', flat=True)
    avg_fc_parallel = round(np.mean(qs_fc_parallel_list), 2)
    qs_fc_MPA_parallel = qs_parallel.values_list('fc_MPa', flat=True)
    avg_fc_MPA_parallel = round(np.mean(qs_fc_MPA_parallel), 2)

    if avg_fc_MPA_parallel >= 7.8 and avg_fc_MPA_parallel < 10.8:
        type_parallel = "Grupo C"
    elif avg_fc_MPA_parallel >= 10.8 and avg_fc_MPA_parallel < 14.2:
        type_parallel = "Grupo B"
    elif avg_fc_MPA_parallel >= 14.2:
        type_parallel = "Grupo A"
    else:
        type_parallel = "No Evalua para un Grupo"

    # Perpendicular
    qs_perpendicular = qs_parallel_perpendicular.filter(type_compression="PERPENDICULAR")
    qs_fc_perpendicular_list = qs_perpendicular.values_list('fc', flat=True)
    avg_fc_perpendicular = round(np.mean(qs_fc_perpendicular_list), 2)
    qs_fc_MPA_perpendicular = qs_perpendicular.values_list('fc_MPa', flat=True)
    avg_fc_MPA_perpendicular = round(np.mean(qs_fc_MPA_perpendicular), 2)

    if avg_fc_MPA_perpendicular >= 1.5 and avg_fc_MPA_perpendicular < 2.7:
        type_perpendicular = "Grupo C"
    elif avg_fc_MPA_perpendicular >= 2.7 and avg_fc_MPA_perpendicular < 3.9:
        type_perpendicular = "Grupo B"
    elif avg_fc_MPA_perpendicular >= 3.9:
        type_perpendicular = "Grupo A"
    else:
        type_perpendicular = "No Evalua para un Grupo"

    context = {
        "obj": obj,
        # Parallel
        "qs_parallel": qs_parallel,
        "avg_fc_parallel": avg_fc_parallel,
        "avg_fc_MPA_parallel": avg_fc_MPA_parallel,
        "norma_NTP_parallel": "NTP 251.014",
        "type_parallel": type_parallel,
        # Parallel
        "qs_perpendicular": qs_perpendicular,
        "avg_fc_perpendicular": avg_fc_perpendicular,
        "avg_fc_MPA_perpendicular": avg_fc_MPA_perpendicular,
        "norma_NTP_perpendicular": "NTP E-010",
        "type_perpendicular": type_perpendicular,

        "title": "Detalles del EnCompresión Simple Perpendicular o Paralela en Madera",
    }

    return render(request, 'tests_material/wood_compression/wood_compression_detail.html', context)


@login_required
def wood_compression_delete(request, id):
    obj = get_object_or_404(WoodCompression, id=id)
    equips = Equip.objects.filter(name__in=("Balanza", "Maquina Compresora", "Regla Graduada",))

    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_material:wood_compression_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Compresión Simple Perpendicular o Paralela en Madera",
    }

    return render(request, 'tests_material/wood_compression/wood_compression_delete_comfirm.html', context)


@login_required
def wood_compression_pdf(request, id):
    obj = get_object_or_404(WoodCompression, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()

    # Compretion Simple
    qs_parallel_perpendicular = ParallelPerpendicular.objects.filter(wood_compression=obj.id)

    # Parallel
    qs_parallel = qs_parallel_perpendicular.filter(type_compression="PARALELO")
    qs_fc_parallel_list = qs_parallel.values_list('fc', flat=True)
    avg_fc_parallel = round(np.mean(qs_fc_parallel_list), 2)
    qs_fc_MPA_parallel = qs_parallel.values_list('fc_MPa', flat=True)
    avg_fc_MPA_parallel = round(np.mean(qs_fc_MPA_parallel), 2)

    if avg_fc_MPA_parallel >= 7.8 and avg_fc_MPA_parallel < 10.8:
        type_parallel = "Grupo C"
    elif avg_fc_MPA_parallel >= 10.8 and avg_fc_MPA_parallel < 14.2:
        type_parallel = "Grupo B"
    elif avg_fc_MPA_parallel >= 14.2:
        type_parallel = "Grupo A"
    else:
        type_parallel = "No Evalua para un Grupo"

    # Perpendicular
    qs_perpendicular = qs_parallel_perpendicular.filter(type_compression="PERPENDICULAR")
    qs_fc_perpendicular_list = qs_perpendicular.values_list('fc', flat=True)
    avg_fc_perpendicular = round(np.mean(qs_fc_perpendicular_list), 2)
    qs_fc_MPA_perpendicular = qs_perpendicular.values_list('fc_MPa', flat=True)
    avg_fc_MPA_perpendicular = round(np.mean(qs_fc_MPA_perpendicular), 2)

    if avg_fc_MPA_perpendicular >= 1.5 and avg_fc_MPA_perpendicular < 2.7:
        type_perpendicular = "Grupo C"
    elif avg_fc_MPA_perpendicular >= 2.7 and avg_fc_MPA_perpendicular < 3.9:
        type_perpendicular = "Grupo B"
    elif avg_fc_MPA_perpendicular >= 3.9:
        type_perpendicular = "Grupo A"
    else:
        type_perpendicular = "No Evalua para un Grupo"

    context = {
        "obj": obj,
        # Parallel
        "qs_parallel": qs_parallel,
        "avg_fc_parallel": avg_fc_parallel,
        "avg_fc_MPA_parallel": avg_fc_MPA_parallel,
        "norma_NTP_parallel": "NTP 251.014",
        "type_parallel": type_parallel,
        # Parallel
        "qs_perpendicular": qs_perpendicular,
        "avg_fc_perpendicular": avg_fc_perpendicular,
        "avg_fc_MPA_perpendicular": avg_fc_MPA_perpendicular,
        "norma_NTP_perpendicular": "NTP E-010",
        "type_perpendicular": type_perpendicular,

        "title": "DETERMINAR LAS Compresión Simple Perpendicular o Paralela en Madera",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_material/wood_compression/wood_compression_pdf.html', context)
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
