from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np

from tests_soil.models import FineMaterial
from tests_soil.forms import FineMaterialForm, FineMaterialFormClient
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def fine_material_list(request):

    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = FineMaterial.objects.filter(user=request.user)
        context = {
            "file_name": "Determinación_Material_Mas_Fino",
            "title": "Ensayos de Determinación del Material más Fino que Pasa la Malla Nª200",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/fine_material/fine_material_list.html', context) 

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = FineMaterial.objects.all()
        context = {
            "file_name": "Determinación_Material_Mas_Fino",
            "title": "Ensayos de Determinación del Material más Fino que Pasa la Malla Nª200",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/fine_material/fine_material_list.html', context)        


@login_required
def fine_material_create(request):

    if request.user.is_bach or request.user.is_group:
        form = FineMaterialForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Horno eléctrico", "Balanza", "Tamiz No 4", "Tamiz No 200"))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:fine_material_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = FineMaterialFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Horno eléctrico", "Balanza", "Tamiz No 4", "Tamiz No 200"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:fine_material_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Determinación del Material más Fino que Pasa la Malla Nª200",
    }

    return render(request, "tests_soil/fine_material/fine_material_form.html", context)


@login_required
def fine_material_update(request, id):

    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(FineMaterial, id=id)
        form = FineMaterialForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:fine_material_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(FineMaterial, id=id)
        form = FineMaterialFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:fine_material_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Determinación del Material más Fino que Pasa la Malla Nª200",
    }

    return render(request, "tests_soil/fine_material/fine_material_form.html", context)


@login_required
def fine_material_detail(request, id):
    obj = get_object_or_404(FineMaterial, id=id)

    context = {
        "obj": obj,
        "norma_ASTM": "",
        "noma_NTP": "NTP 400.018",
        "title": "Detalles del Ensayo Determinación del Material más Fino que Pasa la Malla Nª200",
    }

    return render(request, 'tests_soil/fine_material/fine_material_detail.html', context)


@login_required
def fine_material_delete(request, id):
    obj = get_object_or_404(FineMaterial, id=id)
    equips = Equip.objects.filter(name__in=("Horno eléctrico", "Balanza", "Tamiz No 4", "Tamiz No 200"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:fine_material_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo Determinación del Material más Fino que Pasa la Malla Nª200",
    }

    return render(request, 'tests_soil/fine_material/fine_material_delete_comfirm.html', context)


@login_required
def fine_material_pdf(request, id):
    obj = get_object_or_404(FineMaterial, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first() 

    context = {
        "obj": obj,
        "title": "DETERMINACIÓN DE MATERIAL MAS FINO QUE EL TAMIZ 75μm (Nro. 200) EN SUELOS MTC E137",
        "norma_ASTM": "",
        "noma_NTP": "NTP 400.018",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/fine_material/fine_material_pdf.html', context)
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
