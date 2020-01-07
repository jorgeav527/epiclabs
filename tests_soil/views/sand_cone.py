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

from tests_soil.models import SandCone, HumidDensity, ContentMoisture, ContentMoistureCarbure, CorrectionSandCone
from tests_soil.forms import SandConeForm, SandConeFormClient, HumidDensityFormSet, ContentMoistureFormSet, ContentMoistureCarbureFormSet, CorrectionSandConeFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def sand_cone_list(request):

    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = SandCone.objects.filter(user=request.user)
        context = {
            "file_name": "Densidad_Peso_Unitario_Suelo_In_Situ_Método_Cono_Arena",
            "title": "Ensayos de Densidad del Peso Unitario In Situ Método del Cono de Arena",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/sand_cone/sand_cone_list.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = SandCone.objects.all()
        context = {
            "file_name": "Densidad_Peso_Unitario_Suelo_In_Situ_Método_Cono_Arena",
            "title": "Ensayos de Densidad del Peso Unitario In Situ Método del Cono de Arena",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/sand_cone/sand_cone_list.html', context)        


@login_required
def sand_cone_create(request):

    if request.user.is_bach or request.user.is_group:
        form = SandConeForm(request.POST or None)
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
                return redirect('tests_soil:sand_cone_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = SandConeFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Maquinas Varias",))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:sand_cone_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Densidad del Peso Unitario In Situ Método del Cono de Arena",
    }

    return render(request, "tests_soil/sand_cone/sand_cone_form.html", context)


@login_required
def humid_density_save(request, id):
    obj = get_object_or_404(SandCone, id=id)
    equips = Equip.objects.filter(name__in=("Cono de Arena", "Balanza", "Horno Eléctrico",))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = HumidDensityFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:humid_density_save', id=obj.id)
    
    formset = HumidDensityFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayo de Densidad Húmeda, Metodo Cono de Arena",
    }

    return render(request, "tests_soil/sand_cone/humid_density_form.html", context)


@login_required
def content_moisture_save(request, id):
    obj = get_object_or_404(SandCone, id=id)
    equips = Equip.objects.filter(name__in=("Maquinas Varias", "Balanza", "Horno Eléctrico",))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = ContentMoistureFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:content_moisture_save', id=obj.id)
    
    formset = ContentMoistureFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayo de Contenido de Húmedad",
    }

    return render(request, "tests_soil/sand_cone/content_moisture_form.html", context)


@login_required
def moisture_carbure_save(request, id):
    obj = get_object_or_404(SandCone, id=id)
    equips = Equip.objects.filter(name__in=("Maquinas Varias", "Balanza", "Speedy"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = ContentMoistureCarbureFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:moisture_carbure_save', id=obj.id)
    
    formset = ContentMoistureCarbureFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayo de Contenido de Húmedad Usando Carbono 14",
    }

    return render(request, "tests_soil/sand_cone/moisture_carbure_form.html", context)


@login_required
def correction_sandcone_save(request, id):
    obj = get_object_or_404(SandCone, id=id)
    equips = Equip.objects.filter(name__in=("Maquinas Varias", "Balanza"))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = CorrectionSandConeFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:correction_sandcone_save', id=obj.id)
    
    formset = CorrectionSandConeFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Correccion del Ensayo",
    }

    return render(request, "tests_soil/sand_cone/correction_sandcone_form.html", context)


@login_required
def sand_cone_update(request, id):

    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(SandCone, id=id)
        form = SandConeForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:sand_cone_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(SandCone, id=id)
        form = SandConeFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:sand_cone_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Densidad del Peso Unitario In Situ Método del Cono de Arena",
    }

    return render(request, "tests_soil/sand_cone/sand_cone_form.html", context)


@login_required
def sand_cone_detail(request, id):
    obj = get_object_or_404(SandCone, id=id)
    humid = HumidDensity.objects.filter(sand_cone=obj.id).first()
    moisture = ContentMoisture.objects.filter(sand_cone=obj.id).first()
    carbure = ContentMoistureCarbure.objects.filter(sand_cone=obj.id).first()
    correction = CorrectionSandCone.objects.filter(sand_cone=obj.id).first()
    
    Peso_muestra_total_humeda = humid.wet_sample_weight
    Densidad_muestra_total_humeda = humid.density_wet_sample
    Contenido_humedad_muestra = moisture.sample_moisture
    Contenido_humedad_frac_peso_seco = carbure.dry_weight_percentage
    peso_fracción_extradimensionada_húmeda = correction.wet_fraction_weight
    P_E_Ap_Frac_Extrad = correction.p_e_ap_frac_extrad
    Abs_Frac_Extrad = correction.per_abs_tails_extrad
    Peso_fracción_extrad_seca = correction.weight_fraction_extrad
    
    if obj.moisture:
        ans_01 = round((Peso_muestra_total_humeda - peso_fracción_extradimensionada_húmeda)/(1 + Contenido_humedad_frac_peso_seco/100), 2)
        ans_02 = round((Peso_fracción_extrad_seca / (Peso_fracción_extrad_seca + ans_01)) * 100, 2) 
        ans_03 = round((ans_01 / (Peso_fracción_extrad_seca + ans_01)) * 100, 2)
        ans_04 = round(ans_02 + ans_03, 2)
        ans_05 = round((ans_03 * Contenido_humedad_frac_peso_seco + ans_02 * Abs_Frac_Extrad) / 100, 1)
        ans_06 = round((Densidad_muestra_total_humeda * 100) / (ans_05 + 100), 2)
        ans_07 = round(Peso_fracción_extrad_seca + ans_01, 2)
        ans_08 = round((ans_06 * P_E_Ap_Frac_Extrad * ans_03) / (100 * P_E_Ap_Frac_Extrad - ans_06 * ans_05), 2)
        ans_09 = round(ans_08 / obj.weight_dry_max * 100, 1)
    else:
        ans_01 = round((Peso_muestra_total_humeda - peso_fracción_extradimensionada_húmeda)/(1 + Contenido_humedad_muestra/100), 2)
        ans_02 = round((Peso_fracción_extrad_seca / (Peso_fracción_extrad_seca + ans_01)) * 100, 2) 
        ans_03 = round((ans_01 / (Peso_fracción_extrad_seca + ans_01)) * 100, 2)
        ans_04 = round(ans_02 + ans_03, 2) 
        ans_05 = round((ans_03 * Contenido_humedad_muestra + ans_02 * Abs_Frac_Extrad) / 100, 1)
        ans_06 = round((Densidad_muestra_total_humeda * 100) / (ans_05 + 100), 2) 
        ans_07 = round(Peso_fracción_extrad_seca + ans_01, 2) 
        ans_08 = round((ans_06 * P_E_Ap_Frac_Extrad * ans_03) / (100 * P_E_Ap_Frac_Extrad - ans_06 * ans_05), 2) 
        ans_09 = round(ans_08 / obj.weight_dry_max * 100, 1)

    context = {
        "obj": obj,
        "humid": humid,
        "moisture": moisture,
        "carbure": carbure,
        "correction": correction,
        "ans_01": ans_01,
        "ans_02": ans_02,
        "ans_03": ans_03,
        "ans_04": ans_04,
        "ans_05": ans_05,
        "ans_06": ans_06,
        "ans_07": ans_07,
        "ans_08": ans_08,
        "ans_09": ans_09,
        "norma_ASTM": "ASTM D 1556",
        "noma_NTP": "NTP 339.143",
        "title": "Detalles del Ensayo de Densidad del Peso Unitario In Situ Método del Cono de Arena",
    }

    return render(request, 'tests_soil/sand_cone/sand_cone_detail.html', context)


@login_required
def sand_cone_delete(request, id):
    obj = get_object_or_404(SandCone, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:sand_cone_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Densidad del Peso Unitario In Situ Método del Cono de Arena",
    }

    return render(request, 'tests_soil/sand_cone/sand_cone_delete_comfirm.html', context)


@login_required
def sand_cone_pdf(request, id):
    obj = get_object_or_404(SandCone, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()
    humid = HumidDensity.objects.filter(sand_cone=obj.id).first()
    moisture = ContentMoisture.objects.filter(sand_cone=obj.id).first()
    carbure = ContentMoistureCarbure.objects.filter(sand_cone=obj.id).first()
    correction = CorrectionSandCone.objects.filter(sand_cone=obj.id).first()
    
    Peso_muestra_total_humeda = humid.wet_sample_weight
    Densidad_muestra_total_humeda = humid.density_wet_sample
    Contenido_humedad_muestra = moisture.sample_moisture
    Contenido_humedad_frac_peso_seco = carbure.dry_weight_percentage
    peso_fracción_extradimensionada_húmeda = correction.wet_fraction_weight
    P_E_Ap_Frac_Extrad = correction.p_e_ap_frac_extrad
    Abs_Frac_Extrad = correction.per_abs_tails_extrad
    Peso_fracción_extrad_seca = correction.weight_fraction_extrad
    
    if obj.moisture:
        ans_01 = round((Peso_muestra_total_humeda - peso_fracción_extradimensionada_húmeda)/(1 + Contenido_humedad_frac_peso_seco/100), 2)
        ans_02 = round((Peso_fracción_extrad_seca / (Peso_fracción_extrad_seca + ans_01)) * 100, 2) 
        ans_03 = round((ans_01 / (Peso_fracción_extrad_seca + ans_01)) * 100, 2)
        ans_04 = round(ans_02 + ans_03, 2) 
        ans_05 = round((ans_03 * Contenido_humedad_frac_peso_seco + ans_02 * Abs_Frac_Extrad) / 100, 1)
        ans_06 = round((Densidad_muestra_total_humeda * 100) / (ans_05 + 100), 2) 
        ans_07 = round(Peso_fracción_extrad_seca + ans_01, 2) 
        ans_08 = round((ans_06 * P_E_Ap_Frac_Extrad * ans_03) / (100 * P_E_Ap_Frac_Extrad - ans_06 * ans_05), 2) 
        ans_09 = round(ans_08 / obj.weight_dry_max * 100, 1)
    else:
        ans_01 = round((Peso_muestra_total_humeda - peso_fracción_extradimensionada_húmeda)/(1 + Contenido_humedad_muestra/100), 2)
        ans_02 = round((Peso_fracción_extrad_seca / (Peso_fracción_extrad_seca + ans_01)) * 100, 2) 
        ans_03 = round((ans_01 / (Peso_fracción_extrad_seca + ans_01)) * 100, 2)
        ans_04 = round(ans_02 + ans_03, 2) 
        ans_05 = round((ans_03 * Contenido_humedad_muestra + ans_02 * Abs_Frac_Extrad) / 100, 1)
        ans_06 = round((Densidad_muestra_total_humeda * 100) / (ans_05 + 100), 2) 
        ans_07 = round(Peso_fracción_extrad_seca + ans_01, 2) 
        ans_08 = round((ans_06 * P_E_Ap_Frac_Extrad * ans_03) / (100 * P_E_Ap_Frac_Extrad - ans_06 * ans_05), 2) 
        ans_09 = round(ans_08 / obj.weight_dry_max * 100, 1)

    context = {
        "obj": obj,
        "title": "ENSAYO PARA DETERMINAR LA DENSIDAD Y PESO UNITARIO DEL SUELO IN SITU MEDIANTE EL MÉTODO DEL CONO DE ARENA - MTC E117",
        "humid": humid,
        "moisture": moisture,
        "carbure": carbure,
        "correction": correction,
        "ans_01": ans_01,
        "ans_02": ans_02,
        "ans_03": ans_03,
        "ans_04": ans_04,
        "ans_05": ans_05,
        "ans_06": ans_06,
        "ans_07": ans_07,
        "ans_08": ans_08,
        "ans_09": ans_09,
        "norma_ASTM": "ASTM D 1556",
        "noma_NTP": "NTP 339.143",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/sand_cone/sand_cone_pdf.html', context)
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


