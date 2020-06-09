from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np

from tests_material.models import MasonryCompression, Masonry
from tests_material.forms import MasonryCompressionForm, MasonryCompressionFormClient, MasonryFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

@login_required
def masonry_compression_list(request):

    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = MasonryCompression.objects.filter(user=request.user)
        context = {
            "file_name": "Compresion_Pilas_Muretes",
            "title": "Ensayos de Compresión de Prismas de Albañileria",
            "obj_list": obj_list,
        }
        return render(request, 'tests_material/masonry_compression/masonry_compression_list.html', context)        

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = MasonryCompression.objects.all()
        context = {
            "file_name": "Compresion_Pilas_Muretes",
            "title": "Ensayos de Compresión de Prismas de Albañileria",
            "obj_list": obj_list,
        }
        return render(request, 'tests_material/masonry_compression/masonry_compression_list.html', context)        


@login_required
def masonry_compression_create(request):

    if request.user.is_bach or request.user.is_group:
        form = MasonryCompressionForm(request.POST or None)
        equip = Equip.objects.get(name="Carro de Mano",)
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                form.instance.equipment.add(equip)
                equip.use = F("use") + 1 # equip.use += 1
                equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_material:masonry_compression_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = MasonryCompressionFormClient(request.POST or None)
        equip = Equip.objects.get(name="Carro de Mano",)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                form.instance.equipment.add(equip)
                equip.use = F("use") + 1 # equip.use += 1
                equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_material:masonry_compression_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Compresión de Prismas de Albañileria",
    }

    return render(request, "tests_material/masonry_compression/masonry_compression_form.html", context)


@login_required
def masonry_save(request, id):
    obj = get_object_or_404(MasonryCompression, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Regla Graduada",))

    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = MasonryFormSet(request.POST, instance=obj)
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
                return redirect('tests_material:masonry_save', id=obj.id)
    
    formset = MasonryFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Determinación de Variación de Dimenciones",
    }

    return render(request, "tests_material/masonry_compression/masonry_form.html", context)


@login_required
def masonry_compression_update(request, id):

    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(MasonryCompression, id=id)
        form = MasonryCompressionForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_material:masonry_compression_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(MasonryCompression, id=id)
        form = MasonryCompressionFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_material:masonry_compression_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Compresión de Prismas de Albañileria",
    }

    return render(request, "tests_material/masonry_compression/masonry_compression_form.html", context)


@login_required
def masonry_compression_detail(request, id):
    obj = get_object_or_404(MasonryCompression, id=id)

    # Compretion Simple
    qs_masonry = Masonry.objects.filter(masonry_compression=obj.id)

    # fb Compression
    qs_fc_masonry = qs_masonry.values_list('fc', flat=True)
    avg_fc = round(np.mean(qs_fc_masonry), 2)
    qs_fc_MPA = qs_masonry.values_list('fc_MPa', flat=True)
    avg_fc_MPA = round(np.mean(qs_fc_MPA), 1)

    context = {
        "obj": obj,
        "qs_masonry": qs_masonry,
        # fb Compression
        "avg_fc": avg_fc,
        "avg_fc_MPA": avg_fc_MPA,
        "norma_NTP_fb": "NTP 251.014",

        "title": "Detalles del EnCompresión de Prismas de Albañileria",
    }

    return render(request, 'tests_material/masonry_compression/masonry_compression_detail.html', context)


@login_required
def masonry_compression_delete(request, id):
    obj = get_object_or_404(MasonryCompression, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Regla Graduada",))

    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_material:masonry_compression_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Compresión de Prismas de Albañileria",
    }

    return render(request, 'tests_material/masonry_compression/masonry_compression_delete_comfirm.html', context)


@login_required
def masonry_compression_pdf(request, id):
    obj = get_object_or_404(MasonryCompression, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first()

    # Compretion Simple
    qs_masonry = Masonry.objects.filter(masonry_compression=obj.id)

    # fb Compression
    qs_fc_masonry = qs_masonry.values_list('fc', flat=True)
    avg_fc = round(np.mean(qs_fc_masonry), 2)
    qs_fc_MPA = qs_masonry.values_list('fc_MPa', flat=True)
    avg_fc_MPA = round(np.mean(qs_fc_MPA), 1)

    context = {
        "obj": obj,
        "obj": obj,
        "qs_masonry": qs_masonry,
        # fb Compression
        "avg_fc": avg_fc,
        "avg_fc_MPA": avg_fc_MPA,
        "norma_NTP_fb": "NTP 251.014",

        "title": "MÉTODO DE ENSAYO PARA LA DETERMINACIÓN DE LA RESISTENCIA EN COMPRESIÓN DE PRISMAS DE ALBAÑILERIA",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_material/masonry_compression/masonry_compression_pdf.html', context)
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
