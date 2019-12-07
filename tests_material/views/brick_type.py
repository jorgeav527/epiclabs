from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
# import pdfkit
from django.template.loader import render_to_string
from weasyprint import HTML
from django.template.loader import get_template
from django.db.models import F
from django.contrib.auth.decorators import login_required
import numpy as np

from tests_material.models import BrickType, VariationDimensions, Warping, DensityVoids, Suction, AbsSatuCoeff, CompretionBrick
from tests_material.forms import BrickTypeForm, BrickTypeFormClient, VadriationDimensionsFormSet, WarpingFormSet, DensityVoidsFormSet, SuctionFormSet, AbsSatuCoeffFormSet, CompretionBrickFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

@login_required
def brick_type_list(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        obj_list = BrickType.objects.filter(user=request.user)
        context = {
            "file_name": "Propiedades_Tipo_del_Ladrillo",
            "title": "Ensayos de Propiedades en Unidades de Albañileria Calcinada para la Construcción",
            "obj_list": obj_list,
        }
        return render(request, 'tests_material/brick_type/brick_type_list.html', context)        

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = BrickType.objects.all()
        context = {
            "file_name": "Propiedades_Tipo_del_Ladrillo",
            "title": "Ensayos de Propiedades en Unidades de Albañileria Calcinada para la Construcción",
            "obj_list": obj_list,
        }
        return render(request, 'tests_material/brick_type/brick_type_list.html', context)        


@login_required
def brick_type_create(request):

    if request.user.is_bach or request.user.is_student:
        form = BrickTypeForm(request.POST or None)
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
                return redirect('tests_material:brick_type_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = BrickTypeFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Balanza", "Maquinas Varias",))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_material:brick_type_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Propiedades en Unidades de Albañileria Calcinada para la Construcción",
    }

    return render(request, "tests_material/brick_type/brick_type_form.html", context)


@login_required
def variation_dimensions_save(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Regla Graduada", "Cuñas de medición",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = VadriationDimensionsFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_material:variation_dimensions_save', id=obj.id)
    
    formset = VadriationDimensionsFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación de Variación de Dimenciones",
    }

    return render(request, "tests_material/brick_type/variation_dimensions_form.html", context)


@login_required
def warping_save(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Regla Graduada", "Cuñas de medición",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = WarpingFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_material:warping_save', id=obj.id)
    
    formset = WarpingFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación del Alabeo",
    }

    return render(request, "tests_material/brick_type/warping_form.html", context)


@login_required
def density_voids_save(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Regla Graduada", "Balanza",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = DensityVoidsFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_material:density_voids_save', id=obj.id)
    
    formset = DensityVoidsFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación de la Densidad y el Porcentaje de Vacios",
    }

    return render(request, "tests_material/brick_type/density_voids_form.html", context)


@login_required
def suction_save(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Cronómetro",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = SuctionFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_material:suction_save', id=obj.id)
    
    formset = SuctionFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación de la Succión",
    }

    return render(request, "tests_material/brick_type/suction_form.html", context)


@login_required
def abs_satu_coeff_save(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Cocina",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = AbsSatuCoeffFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_material:abs_satu_coeff_save', id=obj.id)
    
    formset = AbsSatuCoeffFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación del Absorción y el Coeficiente de Saturación",
    }

    return render(request, "tests_material/brick_type/abs_satu_coeff_form.html", context)


@login_required
def compretion_brick_save(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Maquina Compresora",))

    if request.user.is_bach or request.user.is_student or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = CompretionBrickFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                    for equip in equips:    
                        instance.equipment.add(equip)
                        equip.use = F("use") + 1
                        equip.save()
                messages.success(request, f"Los ensayos han sido creados")
                return redirect('tests_material:compretion_brick_save', id=obj.id)
    
    formset = CompretionBrickFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación de la Resistencia a la Compresión",
    }

    return render(request, "tests_material/brick_type/compretion_brick_form.html", context)


@login_required
def brick_type_update(request, id):

    if request.user.is_bach or request.user.is_student:
        obj = get_object_or_404(BrickType, id=id)
        form = BrickTypeForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_material:brick_type_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(BrickType, id=id)
        form = BrickTypeFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_material:brick_type_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Propiedades en Unidades de Albañileria Calcinada para la Construcción",
    }

    return render(request, "tests_material/brick_type/brick_type_form.html", context)


@login_required
def brick_type_detail(request, id):
    obj = get_object_or_404(BrickType, id=id)

    # Variation dimentions
    qs_variation_dimentions = VariationDimensions.objects.filter(brick_type=obj.id)

    qs_avg_length_vd_list = qs_variation_dimentions.values_list('average_length', flat=True) 
    avg_length_vd = round(np.mean(qs_avg_length_vd_list), 2)
    vd_lengt = round(((obj.n_d_length - avg_length_vd) / avg_length_vd) * 100, 2)

    qs_avg_width_vd_list = qs_variation_dimentions.values_list('average_width', flat=True) 
    avg_width_vd = round(np.mean(qs_avg_width_vd_list), 2)
    vd_width = round(((obj.n_d_width - avg_width_vd) / avg_width_vd) * 100, 2)

    qs_avg_high_vd_list = qs_variation_dimentions.values_list('average_high', flat=True) 
    avg_high_vd = round(np.mean(qs_avg_high_vd_list), 2)
    vd_high = round(((obj.n_d_high - avg_high_vd) / avg_high_vd) * 100, 2)

    # Warping
    qs_warping = Warping.objects.filter(brick_type=obj.id)

    qs_upface_concave_list = qs_warping.values_list('upface_concave', flat=True) 
    qs_upface_convex_list = qs_warping.values_list('upface_convex', flat=True) 
    qs_downface_concave_list = qs_warping.values_list('downface_concave', flat=True) 
    qs_downface_convex_list = qs_warping.values_list('downface_convex', flat=True) 


    avg_upface_concave = round(np.mean(qs_upface_concave_list), 2)
    avg_upface_convex = round(np.mean(qs_upface_convex_list), 2)
    avg_downface_concave = round(np.mean(qs_downface_concave_list), 2)
    avg_downface_convex = round(np.mean(qs_downface_convex_list), 2)
    max_avg_warping = max(avg_upface_concave, avg_upface_convex, avg_downface_concave, avg_downface_convex,)

    if max_avg_warping <= 2:
        type_warping = "Ladrillo V"
    elif max_avg_warping <= 4:
        type_warping = "Ladrillo IV"
    elif max_avg_warping <= 6:
        type_warping = "Ladrillo III"
    elif max_avg_warping <= 8:
        type_warping = "Ladrillo II"
    elif max_avg_warping <= 10:
        type_warping = "Ladrillo I"
    else:
        type_warping = "Ladrillo Desconocido"

    # Density Voids
    qs_density_voids = DensityVoids.objects.filter(brick_type=obj.id)

    qs_void_percentage_list = qs_density_voids.values_list('void_percentage', flat=True)
    qs_density_list = qs_density_voids.values_list('density', flat=True)

    avg_void_percentage = round(np.mean(qs_void_percentage_list), 0)
    avg_density = round(np.mean(qs_density_list), 2)

    if avg_density >= 1.70:
        type_density = "Ladrillo V"
    elif avg_density >= 1.65:
        type_density = "Ladrillo IV"
    elif avg_density >= 1.60:
        type_density = "Ladrillo III"
    elif avg_density >= 1.55:
        type_density = "Ladrillo II"
    elif avg_density >= 1.50:
        type_density = "Ladrillo I"
    else:
        type_density = "Ladrillo Desconocido"

    # Suction
    qs_suction = Suction.objects.filter(brick_type=obj.id)

    qs_face_wet_weight_correction_list = qs_suction.values_list('face_wet_weight_correction', flat=True)
    avg_face_wet_weight_correction = round(np.mean(qs_face_wet_weight_correction_list), 2)

    # Absortion and Coeff of Sat 
    qs_abs_sat_coff = AbsSatuCoeff.objects.filter(brick_type=obj.id)
    qs_abs_brick_list = qs_abs_sat_coff.values_list('abs_brick', flat=True)
    qs_abs_max_brick_list = qs_abs_sat_coff.values_list('abs_max_brick', flat=True)
    qs_coeff_sat_list = qs_abs_sat_coff.values_list('coeff_sat', flat=True)
    avg_abs_brick = round(np.mean(qs_abs_brick_list), 2)
    avg_abs_max_brick = round(np.mean(qs_abs_max_brick_list), 2)
    avg_coeff_sat = round(np.mean(qs_coeff_sat_list), 2)

    if avg_abs_brick <= 22:
        type_abs = "Ladrillo V"
    elif avg_abs_brick <= 23:
        type_abs = "Ladrillo IV"
    elif avg_abs_brick <= 25:
        type_abs = "Ladrillo III"
    elif avg_abs_brick <= 27:
        type_abs = "Ladrillo II"
    elif avg_abs_brick <= 30:
        type_abs = "Ladrillo I"
    else:
        type_abs = "Ladrillo Desconocido"

    if avg_coeff_sat <= 0.88:
        type_coeff_sat = "Ladrillo V"
    elif avg_coeff_sat <= 0.89:
        type_coeff_sat = "Ladrillo IV"
    elif avg_coeff_sat <= 0.90:
        type_coeff_sat = "Ladrillo III"
    elif avg_coeff_sat <= 0.91:
        type_coeff_sat = "Ladrillo II"
    elif avg_coeff_sat >= 0.92:
        type_coeff_sat = "Ladrillo I"
    else:
        type_coeff_sat = "Ladrillo Desconocido"

    # Compretion Brick
    qs_compretion_brick = CompretionBrick.objects.filter(brick_type=obj.id)
    qs_fc_list = qs_compretion_brick.values_list('fc', flat=True)
    avg_fc = round(np.mean(qs_fc_list), 2)
    qs_fc_MPA = qs_compretion_brick.values_list('fc_MPa', flat=True)
    avg_fc_MPA = round(np.mean(qs_fc_MPA), 2)

    if avg_fc_MPA <= 17.6 and avg_fc_MPA > 12.7:
        type_compretion = "Ladrillo V"
    elif avg_fc_MPA <= 12.7 and avg_fc_MPA > 9.3:
        type_compretion = "Ladrillo IV"
    elif avg_fc_MPA <= 9.3 and avg_fc_MPA > 6.9:
        type_compretion = "Ladrillo III"
    elif avg_fc_MPA <= 6.9 and avg_fc_MPA > 4.9:
        type_compretion = "Ladrillo II"
    elif avg_fc_MPA <= 4.9:
        type_compretion = "Ladrillo I"
    else:
        type_compretion = "Ladrillo Desconosido"

    context = {
        "obj": obj,
        # Variation dimentions
        "qs_variation_dimentions": qs_variation_dimentions,
        "vd_lengt": vd_lengt,
        "vd_width": vd_width,
        "vd_high": vd_high,
        "norma_NTP_variation_dimentions": "NTP 339.613",
        # Warping
        "qs_warping": qs_warping,
        "avg_upface_concave": avg_upface_concave,
        "avg_upface_convex": avg_upface_convex,
        "avg_downface_concave": avg_downface_concave,
        "avg_downface_convex": avg_downface_convex,
        "type_warping": type_warping,
        "max_avg_warping": max_avg_warping,
        "norma_NTP_qs_warping": "NTP 339.613",
        # Density Voids        
        "qs_density_voids": qs_density_voids,
        "avg_void_percentage": avg_void_percentage,
        "avg_density": avg_density,
        "type_density": type_density,
        "norma_NTP_density_voids": "NTP 331.017",
        # Suction
        "qs_suction": qs_suction,
        "avg_face_wet_weight_correction": avg_face_wet_weight_correction,
        "norma_NTP_suction": "NTP 339.613",
        # Abs_sat_coff
        "qs_abs_sat_coff": qs_abs_sat_coff,
        "avg_abs_brick": avg_abs_brick,
        "avg_abs_max_brick": avg_abs_max_brick,
        "avg_coeff_sat": avg_coeff_sat,
        "type_abs": type_abs,
        "type_coeff_sat": type_coeff_sat,
        "norma_NTP_abs_sat_coff": "NTP 331.018",
        # Compretion Brick
        "qs_compretion_brick": qs_compretion_brick,
        "avg_fc": avg_fc,
        "avg_fc_MPA": avg_fc_MPA,
        "type_compretion": type_compretion,
        "norma_NTP_compretion_brick": "NTP 339.604",

        "title": "Detalles del EnPropiedades en Unidades de Albañileria Calcinada para la Construcción",
    }

    return render(request, 'tests_material/brick_type/brick_type_detail.html', context)


@login_required
def brick_type_delete(request, id):
    obj = get_object_or_404(BrickType, id=id)
    equips = Equip.objects.filter(name__in=("Horno Eléctrico", "Balanza", "Maquina Compresora", "Cocina", "Regla Graduada", "Cuñas de medición",))

    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_material:brick_type_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Propiedades en Unidades de Albañileria Calcinada para la Construcción",
    }

    return render(request, 'tests_material/brick_type/brick_type_delete_comfirm.html', context)


@login_required
def brick_type_pdf(request, id):
    obj = get_object_or_404(BrickType, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()

    html = render_to_string('tests_material/brick_type/brick_type_pdf.html', {
        "obj": obj,
        "title": "DETERMINAR LAS PROPIEDADES EN UNIDADES DE ALBAÑILERIA CALCINADA PARA LA CONSTRUCCIÓN",
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



