from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from django.db.models import F
import numpy as np

from tests_concrete.models import PrismBreak, Prism
from tests_concrete.forms import PrismBreakForm, PrismBreakFormClient, PrismFormSet
from equipments.models import Equip
from accounts.models import AdminProfile


# Create your views here.

@login_required
def prism_break_list(request):
    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = PrismBreak.objects.filter(user=request.user)
        context = {
            "file_name": "Rotura_Prisma",
            "title": "Ensayos de Rotura de Prismas",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/prism_break/prism_break_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = PrismBreak.objects.all()
        context = {
            "file_name": "Rotura_Prisma",
            "title": "Ensayos de Rotura de Prismas",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/prism_break/prism_break_list.html', context)        


@login_required
def prism_break_create(request):
    if request.user.is_bach or request.user.is_group:
        form = PrismBreakForm(request.POST or None)
        equip = Equip.objects.get(name="Carro de Mano",)
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                form.instance.equipment.add(equip)
                equip.use = F("use") + 1 # equip.use += 1
                equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:prism_break_list')
    elif request.user.is_superuser or request.user.is_admin:
        form = PrismBreakFormClient(request.POST or None)
        equip = Equip.objects.get(name="Carro de Mano",)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                form.instance.equipment.add(equip)
                equip.use = F("use") + 1 # equip.use += 1
                equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:prism_break_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Rotura de Prismas",
    }

    return render(request, "tests_concrete/prism_break/prism_break_form.html", context)


@login_required
def prism_save(request, id):
    obj = get_object_or_404(PrismBreak, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Regla Graduada",))

    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = PrismFormSet(request.POST, instance=obj)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    check_per = instance.check_per
                    if check_per == False:
                        messages.error(request, f"El testigo no cumple con la perpendicularidad adecuada")
                        return redirect('tests_concrete:prism_save', id=obj.id)
                    else:
                        instance.save()
                        for equip in equips:
                            instance.equipment.add(equip)
                            equip.use = F("use") + 1
                            equip.save()
                        messages.success(request, f"Los ensayos han sido creados o actualizados")
                formset.save()
                return redirect('tests_concrete:prism_save', id=obj.id)
    
    formset = PrismFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayos de Compresión de Prismas",
    }

    return render(request, "tests_concrete/prism_break/prism_form.html", context)


@login_required
def prism_break_update(request, id):
    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(PrismBreak, id=id)
        form = PrismBreakForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_concrete:prism_break_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(PrismBreak, id=id)
        form = PrismBreakFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_concrete:prism_break_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Rotura de Prismas",
    }

    return render(request, "tests_concrete/prism_break/prism_break_form.html", context)


@login_required
def prism_break_detail(request, id):
    obj = get_object_or_404(PrismBreak, id=id)

    # Compretion Simple
    qs_prism = Prism.objects.filter(prism_break=obj.id)

    prism_fc = qs_prism.values_list("fc", flat=True).order_by("id")
    mean_prism_fc = round(np.mean(prism_fc), 2) 
    std_prism_fc = round(np.std(prism_fc), 2)

    prism_element_name = list(qs_prism.values_list("element_name", flat=True).order_by("id"))
    porcentage_off = list(map(lambda x:round((x-obj.fc_esp)/obj.fc_esp*100, 1), prism_fc))
    zippedList = zip(prism_element_name, porcentage_off)


    prism_fc_MPa = qs_prism.values_list("fc_MPa", flat=True).order_by("id")
    mean_prism_fc_MPa = round(np.mean(prism_fc_MPa), 1) 
    std_prism_fc_MPa = round(np.std(prism_fc_MPa), 1)

    context = {
        "obj": obj,
        "qs_prism": qs_prism,
        "mean_prism_fc": mean_prism_fc,
        "std_prism_fc": std_prism_fc,
        "zippedList": zippedList,
        "mean_prism_fc_MPa": mean_prism_fc_MPa,
        "std_prism_fc_MPa": std_prism_fc_MPa,
        "norma_ASTM": "NORMA ASTM C-109",
        "noma_NTP": "NTP 334.034",
        "title": "Detalles del Ensayo de Rotura de Prismas",
    }

    return render(request, 'tests_concrete/prism_break/prism_break_detail.html', context)


@login_required
def prism_break_delete(request, id):
    obj = get_object_or_404(PrismBreak, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Regla Graduada", "Carro de Mano",))

    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_concrete:prism_break_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Rotura de Prismas",
    }

    return render(request, 'tests_concrete/prism_break/prism_break_delete_comfirm.html', context)


@login_required
def prism_break_pdf(request, id):
    obj = get_object_or_404(PrismBreak, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first() 

    # Compretion Simple
    qs_prism = Prism.objects.filter(prism_break=obj.id)
    
    prism_fc = qs_prism.values_list("fc", flat=True).order_by("id")
    mean_prism_fc = round(np.mean(prism_fc), 2) 
    std_prism_fc = round(np.std(prism_fc), 2)

    prism_element_name = list(qs_prism.values_list("element_name", flat=True).order_by("id"))
    porcentage_off = list(map(lambda x:round((x-obj.fc_esp)/obj.fc_esp*100, 1), prism_fc))
    zippedList = zip(prism_element_name, porcentage_off)

    prism_fc_MPa = qs_prism.values_list("fc_MPa", flat=True).order_by("id")
    mean_prism_fc_MPa = round(np.mean(prism_fc_MPa), 1) 
    std_prism_fc_MPa = round(np.std(prism_fc_MPa), 1)

    context = {
        "obj": obj,
        "qs_prism": qs_prism,
        "mean_prism_fc": mean_prism_fc,
        "std_prism_fc": std_prism_fc,
        "zippedList": zippedList,
        "mean_prism_fc_MPa": mean_prism_fc_MPa,
        "std_prism_fc_MPa": std_prism_fc_MPa,
        "title": "CONCRETO. MÉTODO DE ENSAYO NORMALIZADO PARA LA DETERMINACIÓN DE LA RESISTENCIA A LA COMPRESIÓN DE TESTIGOS EN MUESTRAS PRISMÁTICAS.",
        "norma_ASTM": "NORMA ASTM C-109",
        "noma_NTP": "NTP 334.034",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_concrete/prism_break/prism_break_pdf.html', context)
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
