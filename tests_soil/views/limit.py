from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np

from bokeh.plotting import figure
from bokeh.embed import components

from tests_soil.models import Limit, Liquid, Platic
from tests_soil.forms import LimitForm, LimitFormClient, LiquidFormSet, PlasticFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def limit_list(request):
    if request.user.is_bach or request.user.is_student or request.user.is_client:
        obj_list = Limit.objects.filter(user=request.user)
        context = {
            "file_name": "Limite_Liquido_Limite_Plastico",
            "title": "Ensayos de Limite Liquido y Limite Plastico",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/limit/limit_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = Limit.objects.all()
        context = {
            "file_name": "Limite_Liquido_Limite_Plastico",
            "title": "Ensayos de Limite Liquido y Limite Plastico",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/limit/limit_list.html', context)        


@login_required
def limit_create(request):
    if request.user.is_bach or request.user.is_student:
        form = LimitForm(request.POST or None)
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
                return redirect('tests_soil:limit_list')
    elif request.user.is_superuser or request.user.is_admin:
        form = LimitFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:limit_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Limite Liquido y Limite Plastico",
    }

    return render(request, "tests_soil/limit/limit_form.html", context)


@login_required
def liquid_save(request, id):
    obj = get_object_or_404(Limit, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = LiquidFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:liquid_save', id=obj.id)
    
    formset = LiquidFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Limite Liquido",
    }

    return render(request, "tests_soil/limit/liquid_form.html", context)


@login_required
def plastic_save(request, id):
    obj = get_object_or_404(Limit, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = PlasticFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:plastic_save', id=obj.id)
    
    formset = PlasticFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Limite Plastico",
    }

    return render(request, "tests_soil/limit/plastic_form.html", context)


@login_required
def limit_update(request, id):
    if request.user.is_bach or request.user.is_student:
        obj = get_object_or_404(Limit, id=id)
        form = LimitForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:limit_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(Limit, id=id)
        form = LimitFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:limit_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Limite Liquido y Limite Plastico",
    }

    return render(request, "tests_soil/limit/limit_form.html", context)


@login_required
def limit_detail(request, id):
    obj = get_object_or_404(Limit, id=id)
    qs_liquid = Liquid.objects.filter(limit=obj.id)
    qs_plastic = Platic.objects.filter(limit=obj.id)

    # X and Y values in a list format liquid test
    x_hit = qs_liquid.values_list("hit", flat=True).order_by('id')
    y_moisture = qs_liquid.values_list("moisture", flat=True).order_by('id')

    # # regration line manual
    # mean_x_hit = np.mean(x_hit)
    # mean_y_moisture = np.mean(y_moisture)
    # number = 0
    # denom = 0
    # n = len(x_hit)
    # for i in range(n):
    #     number += (x_hit[i] - mean_x_hit) * (y_moisture[i] - mean_y_moisture)
    #     denom += (x_hit[i] - mean_x_hit) ** 2
    # m = number / denom
    # C = mean_y_moisture - (m * mean_x_hit)

    coef_x1 = np.polyfit(x_hit, y_moisture, 1)
    m = coef_x1[0]
    C = coef_x1[1]
    hit_25 = round(m*25 + C, 1)

    # Y values in a list format plastic test
    y_moisture_plastic = qs_plastic.values_list("moisture", flat=True).order_by('id')
    mean_y_moisture_plastic = round(np.mean(y_moisture_plastic), 1)

    # plastic index
    plastic_index = round(hit_25 - mean_y_moisture_plastic, 1)   

    # ploting
    max_x = np.max(x_hit) + 5
    min_x = np.min(x_hit) - 5
    max_y = np.max(y_moisture) + 5
    min_y = np.min(y_moisture) - 5
    x = np.linspace(min_x, max_x, 100)
    y = C + m*x
    TOOLS="hover,crosshair,pan,wheel_zoom,reset,save,"
    plot = figure(x_axis_type="log", x_range=(min_x, max_x), y_range=(min_y, max_y), tools=TOOLS, 
        title="Limite Liquido", x_axis_label= 'Numero de Golpes', y_axis_label= 'Porcentaje de Humedad (%)',
        sizing_mode="scale_width",)
    plot.circle(x_hit, y_moisture, size=8, legend="Resultados")
    plot.line(x, y, line_width=2, legend="Linea de Tendencia", line_dash='dashed')
    plot.circle(25, hit_25, size=8, color="red", legend="25 Golpes")
    script, div = components(plot)

    context = {
        "script": script,
        "div": div,
        "qs_liquid": qs_liquid,
        "qs_plastic": qs_plastic,
        "hit_25": hit_25,
        "mean_y_moisture_plastic": mean_y_moisture_plastic,
        "plastic_index": plastic_index,
        "obj": obj,
        "norma_ASTM": "ASTM C 4318",
        "noma_NTP": "NTP 339.129",
        "title": "Detalles del Ensayo de Limite Liquido y Limite Plastico",
    }

    return render(request, 'tests_soil/limit/limit_detail.html', context)


@login_required
def limit_delete(request, id):
    obj = get_object_or_404(Limit, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:limit_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Limite Liquido y Limite Plastico",
    }

    return render(request, 'tests_soil/limit/limit_delete_comfirm.html', context)


@login_required
def limit_pdf(request, id):
    obj = get_object_or_404(Limit, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()
    qs_liquid = Liquid.objects.filter(limit=obj.id)
    qs_plastic = Platic.objects.filter(limit=obj.id)

    # X and Y values in a list format liquid test
    x_hit = qs_liquid.values_list("hit", flat=True).order_by('id')
    y_moisture = qs_liquid.values_list("moisture", flat=True).order_by('id')
    # regration line
    mean_x_hit = np.mean(x_hit)
    mean_y_moisture = np.mean(y_moisture)
    number = 0
    denom = 0
    n = len(x_hit)
    for i in range(n):
        number += (x_hit[i] - mean_x_hit) * (y_moisture[i] - mean_y_moisture)
        denom += (x_hit[i] - mean_x_hit) ** 2
    m = number / denom
    C = mean_y_moisture - (m * mean_x_hit)
    hit_25 = round(C + m*25, 1)

    # Y values in a list format plastic test
    y_moisture_plastic = qs_plastic.values_list("moisture", flat=True).order_by('id')
    mean_y_moisture_plastic = round(np.mean(y_moisture_plastic), 1)

    # plastic index
    plastic_index =  round(hit_25 - mean_y_moisture_plastic, 1)   

    # ploting
    max_x = np.max(x_hit) + 5
    min_x = np.min(x_hit) - 5
    max_y = np.max(y_moisture) + 10
    min_y = np.min(y_moisture) - 10
    x = np.linspace(min_x, max_x, 100)
    y = C + m*x
    TOOLS="hover,crosshair,pan,wheel_zoom,reset,save,"
    plot = figure(x_axis_type="log", x_range=(min_x, max_x), y_range=(min_y, max_y), tools=TOOLS, 
        title="Limite Liquido", x_axis_label= 'Numero de Golpes', y_axis_label= 'Porcentaje de Humedad (%)',
        sizing_mode="scale_width",)
    plot.circle(x_hit, y_moisture, size=8, legend="Resultados")
    plot.line(x, y, line_width=2, legend="Linea de Tendencia", line_dash='dashed')
    plot.circle(25, hit_25, size=8, color="red", legend="25 Golpes")
    script, div = components(plot)

    context = {
        "qs_liquid": qs_liquid,
        "qs_plastic": qs_plastic,
        "hit_25": hit_25,
        "mean_y_moisture_plastic": mean_y_moisture_plastic,
        "plastic_index": plastic_index,
        "obj": obj,
        "title": "METODO DE ENSAYO PARA DETERMINAR EL LIMITE LÍQUIDO, LIMITE PLÁSTICO E INDICE DE PLASTICIDAD DE SUELOS MTC E110 - MTC E111",
        "norma_ASTM": "ASTM C 4318",
        "noma_NTP": "NTP 339.129",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/limit/limit_pdf.html', context)
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


