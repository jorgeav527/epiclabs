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

from tests_soil.models import ProctorM, DensityWetDry, Correction
from tests_soil.forms import ProctorMForm, ProctorMFormClient, DensityWetDryFormSet, CorrectionFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def proctor_m_list(request):
    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = ProctorM.objects.filter(user=request.user)
        context = {
            "file_name": "Compactación_de_Suelos_Utilizando_una_Energia_Modificada",
            "title": "Ensayos de Compactación de Suelos Utilizando una Energia Modificada",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/proctor_m/proctor_m_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = ProctorM.objects.all()
        context = {
            "file_name": "Compactación_de_Suelos_Utilizando_una_Energia_Modificada",
            "title": "Ensayos de Compactación de Suelos Utilizando una Energia Modificada",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/proctor_m/proctor_m_list.html', context)        


@login_required
def proctor_m_create(request):

    if request.user.is_bach or request.user.is_group:
        form = ProctorMForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Tamiz No 4", "Tamiz 3/4", "Tamiz 3/8"))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:proctor_m_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = ProctorMFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Herramientas varias"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:proctor_m_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Compactación de Suelos Utilizando una Energia Modificada",
    }

    return render(request, "tests_soil/proctor_m/proctor_m_form.html", context)


@login_required
def density_save(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    equips = Equip.objects.filter(name__in=("Horno eléctrico", "Balanza", "Proctor", "Pison", "Contenedores de muestras"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = DensityWetDryFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:density_save', id=obj.id)
    
    formset = DensityWetDryFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Densidad Húmeda y Densidad Seca",
    }

    return render(request, "tests_soil/proctor_m/density_form.html", context)


# @login_required
# def saturation_save(request, id):
#     obj = get_object_or_404(ProctorM, id=id)
#     equips = Equip.objects.filter(name__in=("Maquinas Varias", "Balanza"))
#     if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
#         if request.method == "POST":
#             formset = SaturationFormSet(request.POST, instance=obj)
#             if formset.is_valid():
#                 instances = formset.save(commit=False)
#                 for instance in instances:
#                     instance.save()
#                     for equip in equips:    
#                         instance.equipment.add(equip)
#                         equip.use = F("use") + 1
#                         equip.save()
#                 formset.save()                
#                 messages.success(request, f"Los ensayos han sido creados")
#                 return redirect('tests_soil:saturation_save', id=obj.id)
    
#     formset = SaturationFormSet(instance=obj)

#     context = {
#         "obj": obj,
#         "formset": formset,
#         "title": "Crear Corrección por Saturación (Parte 1)",
#     }

#     return render(request, "tests_soil/proctor_m/saturation_form.html", context)


@login_required
def correction_save(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    equips = Equip.objects.filter(name__in=("Maquinas Varias", "Balanza"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = CorrectionFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:correction_save', id=obj.id)
    
    formset = CorrectionFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Correccion del Ensayo",
    }

    return render(request, "tests_soil/proctor_m/correction_form.html", context)


@login_required
def proctor_m_update(request, id):
    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(ProctorM, id=id)
        form = ProctorMForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:proctor_m_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(ProctorM, id=id)
        form = ProctorMFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:proctor_m_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Compactación de Suelos Utilizando una Energia Modificada",
    }

    return render(request, "tests_soil/proctor_m/proctor_m_form.html", context)


@login_required
def proctor_m_detail(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    qs_density = DensityWetDry.objects.filter(proctor_m=obj.id)

    # X and Y values in a list format
    x_moisture = qs_density.values_list("moisture", flat=True).order_by('id')
    y_dry_density = qs_density.values_list("dry_density", flat=True).order_by('id')

    coef_x2 = np.polyfit(x_moisture, y_dry_density, 3)
    a = coef_x2[0]
    b = coef_x2[1]
    c = coef_x2[2]
    D = coef_x2[3]

    # ploting
    max_x = np.max(x_moisture) 
    min_x = np.min(x_moisture)
    max_y = np.max(y_dry_density)
    min_y = np.min(y_dry_density)
    x = np.linspace(min_x, max_x, 100)
    y = a*x**3 + b*x**2 + c*x + D

    # Max Dry Density Optimum Moisture 
    max_y_dry_density = round(np.max(y), 2) 
    max_x_moisture = round(x[np.argmax(y)], 1)


    if obj.saturation_check and obj.gs:
        qs_saturation = Correction.objects.filter(proctor_m=obj.id)
        # Saturation Curve to 100% densidad agua 1 gf/cm3
        sat_points = [1/((i/100)+(1/obj.gs)) for i in x_moisture]
        max_y_sat = np.max(sat_points)
        min_y_sat = np.min(sat_points)
    elif obj.saturation_check and obj.gs == Null:
        qs_saturation = Correction.objects.filter(proctor_m=obj.id)
        ys_list = qs_saturation.values_list("g_frac_fina_gruesa", flat=True).order_by('id')
        ys = np.max(ys_list)
    else:
        sat_points = None
        qs_saturation = None
        pfe = None
        pf_f_g = None
        correction_moisture = None
        correction_dry_density =None


    if obj.correction_check:
        qs_saturation = Correction.objects.filter(proctor_m=obj.id)
        pfe_list = qs_saturation.values_list("frac_extrad_weight", flat=True).order_by('id')
        pfe = np.max(pfe_list)
        pf_f_g = 100 - pfe
        pefe_list = qs_saturation.values_list("p_sp_frac_extrad", flat=True).order_by('id')
        pefe = np.max(pefe_list)
        moisture_correction_list = qs_saturation.values_list("moisture", flat=True).order_by('id')
        moisture_correction = np.max(moisture_correction_list)
        # Correction
        correction_moisture = round(max_x_moisture*pf_f_g/100+moisture_correction*pfe/100, 1) 
        correction_dry_density = round(100*max_y_dry_density*pefe*0.99821/(max_y_dry_density*pfe+pefe*0.99821*pf_f_g), 2)
    else:
        qs_saturation = None
        pfe = None
        pf_f_g = None
        correction_moisture = None
        correction_dry_density =None


    # ploting
    TOOLS="hover,crosshair,pan,wheel_zoom,reset,save,"
    if obj.saturation_check:    
        plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y_sat), tools=TOOLS, title="Curva Humedad - Densidad Seca", x_axis_label= 'Porcentaje de Humedad (%)', y_axis_label= 'Densidad Seca (g/cm³)', sizing_mode="scale_width",)
        plot.line(x_moisture, sat_points, line_width=2, line_dash='dashed', color="green", legend="Saturación 100%")
        plot.circle(x_moisture, sat_points, size=8, color="green")
    else:
        plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y), tools=TOOLS, title="Curva Humedad - Densidad Seca", x_axis_label= 'Porcentaje de Humedad (%)', y_axis_label= 'Densidad Seca (g/cm³)', sizing_mode="scale_width",)

    plot.circle(x_moisture, y_dry_density, size=8, legend="Resultados")
    plot.line(x, y, line_width=2, line_dash='dashed')
    plot.circle(max_x_moisture, max_y_dry_density, size=8, color="red", legend="Máximo Punto")
    script, div = components(plot)

    context = {
        "script": script,
        "div": div,
        "qs_density": qs_density,
        "max_y_dry_density": max_y_dry_density,
        "max_x_moisture": max_x_moisture,
        "qs_saturation": qs_saturation,
        "pfe": pfe,
        "pf_f_g": pf_f_g,
        "correction_moisture": correction_moisture,
        "correction_dry_density": correction_dry_density,
        "obj": obj,
        "norma_ASTM": "",
        "noma_NTP": "NTP 339.141",
        "title": "Detalles del Ensayo de Compactación de Suelos Utilizando una Energia Modificada",
    }

    return render(request, 'tests_soil/proctor_m/proctor_m_detail.html', context)


@login_required
def proctor_m_delete(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    equips = Equip.objects.filter(name__in=("Tamiz No 4", "Tamiz 3/4", "Tamiz 3/8", "Horno eléctrico", "Balanza", "Proctor", "Pison", "Contenedores de muestras", "Herramientas varias"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:proctor_m_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Compactación de Suelos Utilizando una Energia Modificada",
    }

    return render(request, 'tests_soil/proctor_m/proctor_m_delete_comfirm.html', context)


@login_required
def proctor_m_pdf(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()
    qs_density = DensityWetDry.objects.filter(proctor_m=obj.id)

    # X and Y values in a list format
    x_moisture = qs_density.values_list("moisture", flat=True).order_by('id')
    y_dry_density = qs_density.values_list("dry_density", flat=True).order_by('id')

    coef_x2 = np.polyfit(x_moisture, y_dry_density, 3)
    a = coef_x2[0]
    b = coef_x2[1]
    c = coef_x2[2]
    D = coef_x2[3]

    # ploting
    max_x = np.max(x_moisture) 
    min_x = np.min(x_moisture)
    max_y = np.max(y_dry_density)
    min_y = np.min(y_dry_density)
    x = np.linspace(min_x, max_x, 100)
    y = a*x**3 + b*x**2 + c*x + D

    # Max Dry Density Optimum Moisture 
    max_y_dry_density = round(np.max(y), 2) 
    max_x_moisture = round(x[np.argmax(y)], 1) 


    if obj.saturation_check and obj.gs:
        qs_saturation = Correction.objects.filter(proctor_m=obj.id)
        # Saturation Curve to 100% densidad agua 1 gf/cm3
        sat_points = [1/((i/100)+(1/obj.gs)) for i in x_moisture]
        max_y_sat = np.max(sat_points)
        min_y_sat = np.min(sat_points)
    elif obj.saturation_check and obj.gs == Null:
        qs_saturation = Correction.objects.filter(proctor_m=obj.id)
        ys_list = qs_saturation.values_list("g_frac_fina_gruesa", flat=True).order_by('id')
        ys = np.max(ys_list)
    else:
        qs_saturation = None
        pfe = None
        pf_f_g = None
        correction_moisture = None
        correction_dry_density =None


    if obj.correction_check:
        qs_saturation = Correction.objects.filter(proctor_m=obj.id)
        pfe_list = qs_saturation.values_list("frac_extrad_weight", flat=True).order_by('id')
        pfe = np.max(pfe_list)
        pf_f_g = 100 - pfe
        pefe_list = qs_saturation.values_list("p_sp_frac_extrad", flat=True).order_by('id')
        pefe = np.max(pefe_list)
        moisture_correction_list = qs_saturation.values_list("moisture", flat=True).order_by('id')
        moisture_correction = np.max(moisture_correction_list)
        # Correction
        correction_moisture = round(max_x_moisture*pf_f_g/100+moisture_correction*pfe/100, 1) 
        correction_dry_density = round(100*max_y_dry_density*pefe*0.99821/(max_y_dry_density*pfe+pefe*0.99821*pf_f_g), 2)
    else:
        qs_saturation = None
        pfe = None
        pf_f_g = None
        correction_moisture = None
        correction_dry_density =None

    # ploting
    fig = plt.figure(figsize=(5.5, 4.1), dpi=80)
    if obj.saturation_check:
        plt.xlim(min_x-1, max_x+1)
        plt.ylim(min_y-0.05, max_y_sat+0.1)
    else:
        plt.xlim(min_x-1, max_x+1)
        plt.ylim(min_y-0.05, max_y+0.1)

    plt.grid(b=True, which='both', axis='both')
    
    plt.scatter(x_moisture, y_dry_density, label='Resultados', s=25, c='blue',)
    plt.plot(x, y, color='blue', linestyle='dashed',)
    if obj.saturation_check:    
        plt.plot(x_moisture, sat_points, linestyle='dashed', color="green")
        plt.scatter(x_moisture, sat_points, label='Saturación 100%', s=25, c='green')
    plt.scatter(max_x_moisture, max_y_dry_density, label='Máximo Punto', s=25, c='red',)

    plt.xlabel('Porcentaje de Humedad (%)')
    plt.ylabel('Densidad Seca (g/cm³)')
    plt.title("Curva Humedad - Densidad Seca")
    plt.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    graphic = base64.b64encode(buf.getbuffer()).decode("ascii")

    context = {
        "qs_density": qs_density,
        "max_y_dry_density": max_y_dry_density,
        "max_x_moisture": max_x_moisture,
        "qs_saturation": qs_saturation,
        "pfe": pfe,
        "pf_f_g": pf_f_g,
        "correction_moisture": correction_moisture,
        "correction_dry_density": correction_dry_density,
        "obj": obj,
        "graphic": graphic,
        "title": "COMPACTACION DE SUELOS EN LABORATORIO UTILIZANDO UNA ENERGIA MODIFICADA (2 700 kN-m/m³ (56 000 pie-lbf/pie³)) PROCTOR MODIFICADO MTC E115",
        "norma_ASTM": "",
        "noma_NTP": "NTP 339.141",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/proctor_m/proctor_m_pdf.html', context)
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
