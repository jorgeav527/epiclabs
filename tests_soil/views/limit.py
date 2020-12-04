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

from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from tests_soil.models import Limit, Liquid, Platic
from tests_soil.forms import LimitForm, LimitFormClient, LiquidFormSet, PlasticFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def limit_list(request):
    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = Limit.objects.filter(user=request.user)
        context = {
            "file_name": "Límite_Líquido_Límite_Plástico",
            "title": "Ensayos de Límite Líquido y Límite Plástico",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/limit/limit_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = Limit.objects.all()
        context = {
            "file_name": "Límite_Líquido_Límite_Plástico",
            "title": "Ensayos de Límite Líquido y Límite Plástico",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/limit/limit_list.html', context)        


@login_required
def limit_create(request):
    if request.user.is_bach or request.user.is_group:
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
        "title": "Crear Ensayo de Límite Líquido y Límite Plástico",
    }

    return render(request, "tests_soil/limit/limit_form.html", context)


@login_required
def liquid_save(request, id):
    obj = get_object_or_404(Limit, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = LiquidFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    hit_passed = instance.hit
                    if hit_passed <= 25:
                        instance.save()
                        for equip in equips:    
                            instance.equipment.add(equip)
                            equip.use = F("use") + 1
                            equip.save()
                        messages.warning(request, f"Si el numero de golpes para serrar la ranura es siempre menor de 25 el Límite Líquido no podrá determinarse, y se determinara al suelo como no plástico sin realizar el ensayo de Límite Plástico")
                        messages.success(request, f"Los ensayos han sido creados")
                    else:
                        instance.save()
                        for equip in equips:    
                            instance.equipment.add(equip)
                            equip.use = F("use") + 1
                            equip.save()
                        messages.success(request, f"Los ensayos han sido creados")
                        # return redirect('tests_soil:liquid_save', id=obj.id)
                formset.save()
                return redirect('tests_soil:liquid_save', id=obj.id)
    
    formset = LiquidFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Límite Líquido",
    }

    return render(request, "tests_soil/limit/liquid_form.html", context)


@login_required
def plastic_save(request, id):
    obj = get_object_or_404(Limit, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
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
        "title": "Crear Ensayos de Límite Plástico",
    }

    return render(request, "tests_soil/limit/plastic_form.html", context)


@login_required
def limit_update(request, id):
    if request.user.is_bach or request.user.is_group:
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
        "title": "Actualizar Ensayo de Límite Líquido y Límite Plástico",
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
    hit_25 = round(m*25 + C, 0)

    # Y values in a list format plastic test
    y_moisture_plastic = qs_plastic.values_list("moisture", flat=True).order_by('id')
    mean_y_moisture_plastic = round(np.mean(y_moisture_plastic), 0)

    # plastic index
    count = 0
    for i in x_hit:
        if i <= 25:
            count += 1
        else:
            count += 0
    
    if count == 4:
        plastic_index = "NP (No Plástico)"
    else:
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
        title="Límite Líquido", x_axis_label= 'Numero de Golpes', y_axis_label= 'Porcentaje de Humedad (%)',
        sizing_mode="scale_width",)
    plot.circle(x_hit, y_moisture, size=8, legend="Resultados")
    plot.line(x, y, line_width=2, color='green', legend="Linea de Tendencia", line_dash='dashed')
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
        "norma_ASTM": "",
        "noma_NTP": "NTP 339.129",
        "title": "Detalles del Ensayo de Límite Líquido y Límite Plástico",
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
        "title": "Eliminar el Ensayo de Límite Líquido y Límite Plástico",
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
    hit_25 = round(C + m*25, 0)

    # Y values in a list format plastic test
    y_moisture_plastic = qs_plastic.values_list("moisture", flat=True).order_by('id')
    mean_y_moisture_plastic = round(np.mean(y_moisture_plastic), 0)

    # plastic index
    count = 0
    for i in x_hit:
        if i <= 25:
            count += 1
        else:
            count += 0
    
    if count == 4:
        plastic_index = "NP (No Plástico)"
    else:
        plastic_index = round(hit_25 - mean_y_moisture_plastic, 1) 

    # ploting
    max_x = np.max(x_hit) + 5
    min_x = np.min(x_hit) - 5
    max_y = np.max(y_moisture) + 5
    min_y = np.min(y_moisture) - 5
    x = np.linspace(min_x, max_x, 100)
    y = C + m*x

    fig = plt.figure(figsize=(5.5, 4.1), dpi=80)

    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.xscale('log')
    plt.grid(b=True, which='both', axis='both')
    
    plt.scatter(x_hit, y_moisture, label='Resultados', s=20, c='blue',)
    plt.plot(x, y, color='green', linestyle='dashed', label='Linea de Tendencia')
    plt.scatter(25, hit_25, label='25 Golpes', s=20, c='red',)

    plt.xlabel('Numero de Glopes')
    plt.ylabel('Porcentaje de Humedad (%)')
    plt.title("Límite Líquido")
    plt.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    graphic = base64.b64encode(buf.getbuffer()).decode("ascii")

    context = {
        "qs_liquid": qs_liquid,
        "qs_plastic": qs_plastic,
        "hit_25": hit_25,
        "mean_y_moisture_plastic": mean_y_moisture_plastic,
        "plastic_index": plastic_index,
        "obj": obj,
        "graphic": graphic,
        "title": "METODO DE ENSAYO PARA DETERMINAR EL LIMITE LÍQUIDO, LIMITE PLÁSTICO E INDICE DE PLASTICIDAD DE SUELOS MTC E110 - MTC E111",
        "norma_ASTM": "",
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


