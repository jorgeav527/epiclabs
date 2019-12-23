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

from tests_soil.models import SpecificGravity, FractionPass, FractionRetained
from tests_soil.forms import SpecificGravityForm, SpecificGravityFormClient, FractionPassFormSet, FractionRetainedFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

@login_required
def specific_gravity_list(request):

    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = SpecificGravity.objects.filter(user=request.user)
        context = {
            "file_name": "Gravedad_Especifica_de_los_Solidos",
            "title": "Ensayos de Gravedad Especifica de Solidos mediante el Picometro de Agua",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/specific_gravity/specific_gravity_list.html', context)        

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = SpecificGravity.objects.all()
        context = {
            "file_name": "Gravedad_Especifica_de_los_Solidos",
            "title": "Ensayos de Gravedad Especifica de Solidos mediante el Picometro de Agua",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/specific_gravity/specific_gravity_list.html', context)        


@login_required
def specific_gravity_create(request):

    if request.user.is_bach or request.user.is_group:
        form = SpecificGravityForm(request.POST or None)
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
                return redirect('tests_soil:specific_gravity_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = SpecificGravityFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Maquinas Varias",))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:specific_gravity_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Gravedad Especifica de Solidos mediante el Picometro de Agua",
    }

    return render(request, "tests_soil/specific_gravity/specific_gravity_form.html", context)


@login_required
def fraction_pass_save(request, id):
    obj = get_object_or_404(SpecificGravity, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Fiola",))

    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = FractionPassFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:fraction_pass_save', id=obj.id)
    
    formset = FractionPassFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos del Material Pasante del Tamiz Nº 4",
    }

    return render(request, "tests_soil/specific_gravity/fraction_pass_form.html", context)


@login_required
def fraction_retained_save(request, id):
    obj = get_object_or_404(SpecificGravity, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Fiola",))

    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = FractionRetainedFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:fraction_retained_save', id=obj.id)
    
    formset = FractionRetainedFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos del Material Retenido del Tamiz Nº 4",
    }

    return render(request, "tests_soil/specific_gravity/fraction_retained_form.html", context)


@login_required
def specific_gravity_update(request, id):

    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(SpecificGravity, id=id)
        form = SpecificGravityForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:specific_gravity_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(SpecificGravity, id=id)
        form = SpecificGravityFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:specific_gravity_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Gravedad Especifica de Solidos mediante el Picometro de Agua",
    }

    return render(request, "tests_soil/specific_gravity/specific_gravity_form.html", context)


@login_required
def specific_gravity_detail(request, id):
    obj = get_object_or_404(SpecificGravity, id=id)
    qs_fraction_pass = FractionPass.objects.filter(specific_gravity=obj.id)
    qs_fraction_retained = FractionRetained.objects.filter(specific_gravity=obj.id)
    grav_sp_real_list = qs_fraction_pass.values_list('gravity_specific_real', flat=True).order_by('id')
    mean_grav_sp = round(np.mean(grav_sp_real_list), 3)
    spe_mass_wei_list = qs_fraction_retained.values_list('specific_mass_weight', flat=True).order_by('id')
    mean_spe_mass_wei = round(np.mean(spe_mass_wei_list), 3)
    spe_mass_wei_sss_list = qs_fraction_retained.values_list('specific_mass_weight_sss', flat=True).order_by('id')
    mean_spe_mass_wei_sss = round(np.mean(spe_mass_wei_sss_list), 3)
    spe_mass_wei_app_list = qs_fraction_retained.values_list('specific_mass_weight_app', flat=True).order_by('id')
    mean_spe_mass_wei_app = round(np.mean(spe_mass_wei_app_list), 3)
    absorption_list = qs_fraction_retained.values_list('absorption', flat=True).order_by('id')
    mean_absorption = round(np.mean(absorption_list), 3)
    material_pass_list = qs_fraction_pass.values_list('material_pass', flat=True).order_by('id')
    mean_material_pass = round(np.mean(material_pass_list), 2)
    material_retained_list = qs_fraction_retained.values_list('material_retained', flat=True).order_by('id')
    mean_material_retained = round(np.mean(material_retained_list), 2)
    total_ave_spe_grav = 1/(((mean_material_retained/100)/mean_spe_mass_wei_app)+((mean_material_pass/100)/mean_grav_sp))
    total_average_specific_gravity = round(total_ave_spe_grav, 3)

    context = {
        "obj": obj,
        "qs_fraction_pass": qs_fraction_pass,
        "qs_fraction_retained": qs_fraction_retained,
        "mean_grav_sp": mean_grav_sp,
        "mean_spe_mass_wei": mean_spe_mass_wei,
        "mean_spe_mass_wei_sss": mean_spe_mass_wei_sss,
        "mean_spe_mass_wei_app": mean_spe_mass_wei_app,
        "mean_absorption": mean_absorption,
        "mean_material_pass": mean_material_pass,
        "mean_material_retained": mean_material_retained,
        "total_average_specific_gravity": total_average_specific_gravity,
        "norma_ASTM": "ASTM Ninguna",
        "noma_NTP": "NTP 339.131",
        "title": "Detalles del Ensayo de Gravedad Especifica de Solidos mediante el Picometro de Agua",
    }

    return render(request, 'tests_soil/specific_gravity/specific_gravity_detail.html', context)


@login_required
def specific_gravity_delete(request, id):
    obj = get_object_or_404(SpecificGravity, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Fiola",))

    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:specific_gravity_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Gravedad Especifica de Solidos mediante el Picometro de Agua",
    }

    return render(request, 'tests_soil/specific_gravity/specific_gravity_delete_comfirm.html', context)


@login_required
def specific_gravity_pdf(request, id):
    obj = get_object_or_404(SpecificGravity, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()
    qs_fraction_pass = FractionPass.objects.filter(specific_gravity=obj.id)
    qs_fraction_retained = FractionRetained.objects.filter(specific_gravity=obj.id)
    grav_sp_real_list = qs_fraction_pass.values_list('gravity_specific_real', flat=True).order_by('id')
    mean_grav_sp = round(np.mean(grav_sp_real_list), 3)
    spe_mass_wei_list = qs_fraction_retained.values_list('specific_mass_weight', flat=True).order_by('id')
    mean_spe_mass_wei = round(np.mean(spe_mass_wei_list), 3)
    spe_mass_wei_sss_list = qs_fraction_retained.values_list('specific_mass_weight_sss', flat=True).order_by('id')
    mean_spe_mass_wei_sss = round(np.mean(spe_mass_wei_sss_list), 3)
    spe_mass_wei_app_list = qs_fraction_retained.values_list('specific_mass_weight_app', flat=True).order_by('id')
    mean_spe_mass_wei_app = round(np.mean(spe_mass_wei_app_list), 3)
    absorption_list = qs_fraction_retained.values_list('absorption', flat=True).order_by('id')
    mean_absorption = round(np.mean(absorption_list), 3)
    material_pass_list = qs_fraction_pass.values_list('material_pass', flat=True).order_by('id')
    mean_material_pass = round(np.mean(material_pass_list), 2)
    material_retained_list = qs_fraction_retained.values_list('material_retained', flat=True).order_by('id')
    mean_material_retained = round(np.mean(material_retained_list), 2)
    total_ave_spe_grav = 1/(((mean_material_retained/100)/mean_spe_mass_wei_app)+((mean_material_pass/100)/mean_grav_sp))
    total_average_specific_gravity = round(total_ave_spe_grav, 3)

    context = {
        "obj": obj,
        "mean_grav_sp": mean_grav_sp,
        "mean_spe_mass_wei": mean_spe_mass_wei,
        "mean_spe_mass_wei_sss": mean_spe_mass_wei_sss,
        "mean_spe_mass_wei_app": mean_spe_mass_wei_app,
        "mean_absorption": mean_absorption,
        "mean_material_pass": mean_material_pass,
        "mean_material_retained": mean_material_retained,
        "qs_fraction_pass": qs_fraction_pass,
        "qs_fraction_retained": qs_fraction_retained,
        "total_average_specific_gravity": total_average_specific_gravity,
        "title": "DETERMINACIÓN DE LA GRAVEDAD ESPECIFICA DE SOLIDOS MEDIANTE EL PICOMETRO DE AGUA DE UN SUELO MTC E108",
        "norma_ASTM": "ASTM C2216",
        "noma_NTP": "NTP 339.127",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/specific_gravity/specific_gravity_pdf.html', context)
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
