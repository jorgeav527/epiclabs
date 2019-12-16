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

from tests_soil.models import ProctorM, DensityWetDry, Saturation, Correction
from tests_soil.forms import ProctorMForm, ProctorMFormClient, DensityWetDryFormSet, SaturationFormSet, CorrectionFormSet
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
        equips = Equip.objects.filter(name__in=("Balanza",))
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
        equips = Equip.objects.filter(name__in=("Balanza",))
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
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Proctor", "Pison"))
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


@login_required
def saturation_save(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    equips = Equip.objects.filter(name__in=("Maquinas Varias", "Balanza"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = SaturationFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:saturation_save', id=obj.id)
    
    formset = SaturationFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayo de Saturación",
    }

    return render(request, "tests_soil/proctor_m/saturation_form.html", context)


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
    qs_saturation = Saturation.objects.filter(proctor_m=obj.id)
    qs_correction = Correction.objects.filter(proctor_m=obj.id)

    ys_list = qs_saturation.values_list("g_frac_fina_gruesa", flat=True).order_by('id')
    ys = np.max(ys_list)
    pfe_list = qs_saturation.values_list("frac_extrad_weight", flat=True).order_by('id')
    pfe = np.max(pfe_list)
    pf_f_g = 100 - pfe
    moisture_correction_list = qs_correction.values_list("moisture", flat=True).order_by('id')
    moisture_correction = np.max(moisture_correction_list)
    pefe_list = qs_saturation.values_list("p_sp_frac_extrad", flat=True).order_by('id')
    pefe = np.max(pefe_list)

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

    # Saturation Curve to 100% 80% 60%
    max_w_100 = (((ys/min_y)-1)*100/100*1)/ys*100
    min_w_100 = (((ys/max_y)-1)*100/100*1)/ys*100
    max_w_80 = (((ys/min_y)-1)*80/100*1)/ys*100
    min_w_80 = (((ys/max_y)-1)*80/100*1)/ys*100
    max_w_60 = (((ys/min_y)-1)*60/100*1)/ys*100
    min_w_60 = (((ys/max_y)-1)*60/100*1)/ys*100

    # Correction
    correction_moisture = round(max_x_moisture*pf_f_g/100+moisture_correction*pfe/100, 1) 
    correction_dry_density = round(100*max_y_dry_density*pefe*0.99821/(max_y_dry_density*pfe+pefe*0.99821*pf_f_g), 2) 

    TOOLS="hover,crosshair,pan,wheel_zoom,reset,save,"
    plot = figure(x_range=(min_x-1, max_x+5), y_range=(min_y-0.05, max_y+0.1), tools=TOOLS, 
        title="Curva Humedad - Densidad Seca", x_axis_label= 'Porcentaje de Humedad (%)', y_axis_label= 'Densidad Seca (g/cm³)',
        sizing_mode="scale_width",)
    plot.circle(x_moisture, y_dry_density, size=8, legend="Resultados")
    plot.line(x, y, line_width=2, line_dash='dashed')
    plot.line([max_w_100, min_w_100], [min_y, max_y], line_width=1, line_dash='dashed', color="red")
    plot.line([max_w_80, min_w_80], [min_y, max_y], line_width=1, line_dash='dashed', color="red")
    plot.line([max_w_60, min_w_60], [min_y, max_y], line_width=1, line_dash='dashed', color="red")
    plot.circle(max_x_moisture, max_y_dry_density, size=8, color="red", legend="Maximo Punto")
    script, div = components(plot)

    context = {
        "script": script,
        "div": div,
        "qs_density": qs_density,
        "max_y_dry_density": max_y_dry_density,
        "max_x_moisture": max_x_moisture,
        "qs_saturation": qs_saturation,
        "qs_correction": qs_correction,
        "pfe": pfe,
        "pf_f_g": pf_f_g,
        "correction_moisture": correction_moisture,
        "correction_dry_density": correction_dry_density,
        "obj": obj,
        "norma_ASTM": "ASTM D 1557",
        "noma_NTP": "NTP 339.141",
        "title": "Detalles del Ensayo de Compactación de Suelos Utilizando una Energia Modificada",
    }

    return render(request, 'tests_soil/proctor_m/proctor_m_detail.html', context)


@login_required
def proctor_m_delete(request, id):
    obj = get_object_or_404(ProctorM, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
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
    qs_saturation = Saturation.objects.filter(proctor_m=obj.id)
    qs_correction = Correction.objects.filter(proctor_m=obj.id)

    ys_list = qs_saturation.values_list("g_frac_fina_gruesa", flat=True).order_by('id')
    ys = np.max(ys_list)
    pfe_list = qs_saturation.values_list("frac_extrad_weight", flat=True).order_by('id')
    pfe = np.max(pfe_list)
    pf_f_g = 100 - pfe
    moisture_correction_list = qs_correction.values_list("moisture", flat=True).order_by('id')
    moisture_correction = np.max(moisture_correction_list)
    pefe_list = qs_saturation.values_list("p_sp_frac_extrad", flat=True).order_by('id')
    pefe = np.max(pefe_list)

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

    # Saturation Curve to 100% 80% 60%
    max_w_100 = (((ys/min_y)-1)*100/100*1)/ys*100
    min_w_100 = (((ys/max_y)-1)*100/100*1)/ys*100
    max_w_80 = (((ys/min_y)-1)*80/100*1)/ys*100
    min_w_80 = (((ys/max_y)-1)*80/100*1)/ys*100
    max_w_60 = (((ys/min_y)-1)*60/100*1)/ys*100
    min_w_60 = (((ys/max_y)-1)*60/100*1)/ys*100

    # Correction
    correction_moisture = round(max_x_moisture*pf_f_g/100+moisture_correction*pfe/100, 1) 
    correction_dry_density = round(100*max_y_dry_density*pefe*0.99821/(max_y_dry_density*pfe+pefe*0.99821*pf_f_g), 2) 

    context = {
        "qs_density": qs_density,
        "max_y_dry_density": max_y_dry_density,
        "max_x_moisture": max_x_moisture,
        "qs_saturation": qs_saturation,
        "qs_correction": qs_correction,
        "pfe": pfe,
        "pf_f_g": pf_f_g,
        "correction_moisture": correction_moisture,
        "correction_dry_density": correction_dry_density,
        "obj": obj,
        "title": "COMPACTACION DE SUELOS EN LABORATORIO UTILIZANDO UNA ENERGIA MODIFICADA (2 700 kN-m/m³ (56 000 pie-lbf/pie³)) PROCTOR MODIFICADO MTC E115",
        "norma_ASTM": "ASTM D 1557",
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
