from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
# import pdfkit
from django.template.loader import render_to_string
from weasyprint import HTML
from django.template.loader import get_template
from django.db.models import F
from django.contrib.auth.decorators import login_required
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io.export import get_screenshot_as_png
import numpy as np

from tests_soil.models import MoistureContent, MoistureMaterial
from tests_soil.forms import MoistureContentForm, MoistureContentFormClient, MoistureMaterialFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

@login_required
def moisture_content_list(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        obj_list = MoistureContent.objects.filter(user=request.user)
        context = {
            "file_name": "Contenido_de_Humedad_de_Suelos",
            "title": "Ensayos de Contenido de Humedad",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/moisture_content/moisture_content_list.html', context)        

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = MoistureContent.objects.all()
        context = {
            "file_name": "Contenido_de_Humedad_de_Suelos",
            "title": "Ensayos de Contenido de Humedad",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/moisture_content/moisture_content_list.html', context)        


@login_required
def moisture_content_create(request):

    if request.user.is_bach or request.user.is_student:
        form = MoistureContentForm(request.POST or None)
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
                return redirect('tests_soil:moisture_content_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = MoistureContentFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Maquinas Varias",))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:moisture_content_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Contenido de Humedad",
    }

    return render(request, "tests_soil/moisture_content/moisture_content_form.html", context)


@login_required
def moisture_material_save(request, id):
    obj = get_object_or_404(MoistureContent, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = MoistureMaterialFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_soil:moisture_material_save', id=obj.id)
    
    formset = MoistureMaterialFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Contenido de Humedad del Material",
    }

    return render(request, "tests_soil/moisture_content/moisture_material_form.html", context)


@login_required
def moisture_content_update(request, id):

    if request.user.is_bach or request.user.is_student:
        obj = get_object_or_404(MoistureContent, id=id)
        form = MoistureContentForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:moisture_content_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(MoistureContent, id=id)
        form = MoistureContentFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:moisture_content_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Contenido de Humedad",
    }

    return render(request, "tests_soil/moisture_content/moisture_content_form.html", context)


@login_required
def moisture_content_detail(request, id):
    obj = get_object_or_404(MoistureContent, id=id)
    qs_moisture_material = MoistureMaterial.objects.filter(moisture_content=obj.id)
    qs_gravas = qs_moisture_material.filter(material='GRAVA').order_by('id')
    gravas = qs_gravas.values_list('moisture', flat=True)
    mean_gravas = round(np.mean(gravas), 1)
    qs_finos = qs_moisture_material.filter(material='FINO')
    finos = qs_finos.values_list('moisture', flat=True)
    mean_finos = round(np.mean(finos), 1)
    qs_arenas = qs_moisture_material.filter(material='ARENA')
    arenas = qs_arenas.values_list('moisture', flat=True)
    mean_arenas = round(np.mean(arenas), 1)
    qs_suelos = qs_moisture_material.filter(material='SUELO')
    suelos = qs_suelos.values_list('moisture', flat=True)
    mean_suelos = round(np.mean(suelos), 1)

    context = {
        "obj": obj,
        "qs_gravas": qs_gravas,
        "mean_gravas": mean_gravas,
        "qs_finos": qs_finos,
        "mean_finos": mean_finos,
        "qs_arenas": qs_arenas,
        "mean_arenas": mean_arenas,
        "qs_suelos": qs_suelos,
        "mean_suelos": mean_suelos,
        "norma_ASTM": "ASTM C2216",
        "noma_NTP": "NTP 339.127",
        "title": "Detalles del Ensayo de Contenido de Humedad",
    }

    return render(request, 'tests_soil/moisture_content/moisture_content_detail.html', context)


@login_required
def moisture_content_delete(request, id):
    obj = get_object_or_404(MoistureContent, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))

    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:moisture_content_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Contenido de Humedad",
    }

    return render(request, 'tests_soil/moisture_content/moisture_content_delete_comfirm.html', context)


@login_required
def moisture_content_pdf(request, id):
    obj = get_object_or_404(MoistureContent, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()
    qs_moisture_material = MoistureMaterial.objects.filter(moisture_content=obj.id)
    qs_gravas = qs_moisture_material.filter(material='GRAVA').order_by('id')
    gravas = qs_gravas.values_list('moisture', flat=True)
    mean_gravas = round(np.mean(gravas), 1)
    qs_finos = qs_moisture_material.filter(material='FINO').order_by('id')
    finos = qs_finos.values_list('moisture', flat=True)
    mean_finos = round(np.mean(finos), 1)
    qs_arenas = qs_moisture_material.filter(material='ARENA').order_by('id')
    arenas = qs_arenas.values_list('moisture', flat=True)
    mean_arenas = round(np.mean(arenas), 1)
    qs_suelos = qs_moisture_material.filter(material='SUELO').order_by('id')
    suelos = qs_suelos.values_list('moisture', flat=True)
    mean_suelos = round(np.mean(suelos), 1)

    html = render_to_string('tests_soil/moisture_content/moisture_content_pdf.html', {
        "obj": obj,
        "qs_gravas": qs_gravas,
        "mean_gravas": mean_gravas,
        "qs_finos": qs_finos,
        "mean_finos": mean_finos,
        "qs_arenas": qs_arenas,
        "mean_arenas": mean_arenas,
        "qs_suelos": qs_suelos,
        "mean_suelos": mean_suelos,
        "title": "DETERMINACIÓN DEL CONTENIDO DE HUMEDAD DE UN SUELO MTC E108",
        "norma_ASTM": "ASTM C2216",
        "noma_NTP": "NTP 339.127",
        "coordinator": coordinator,
        "tecnic": tecnic,
    })
    filename = f"Ensayo_{obj.user.username}_{obj.id}.pdf"
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)

    HTML(string=html).write_pdf(response)
    return response



