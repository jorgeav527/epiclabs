from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
# import pdfkit
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from django.template.loader import get_template
from django.db.models import F
from django.contrib.auth.decorators import login_required

from tests_concrete.models import DiamondPiceBreak
from tests_concrete.forms import DiamondPiceBreakForm, DiamondPiceBreakFormClient
from equipments.models import Equip
from accounts.models import AdminProfile

# Create your views here.

@login_required
def diamond_pice_break_list(request):
    if request.user.is_bach or request.user.is_student or request.user.is_client:
        obj_list = DiamondPiceBreak.objects.filter(user=request.user)
        context = {
            "file_name": "Testigos_Diamantinos",
            "title": "Ensayos de Rotura de Testigos Diamantinos",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = DiamondPiceBreak.objects.all()
        context = {
            "file_name": "Testigos_Diamantinos",
            "title": "Ensayos de Rotura de Testigos Diamantinos",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_list.html', context)        


@login_required
def diamond_pice_break_create(request):
    if request.user.is_bach or request.user.is_student:
        form = DiamondPiceBreakForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Maquina Compresora", "Equipo Perforador"))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:diamond_pice_break_list')
    elif request.user.is_superuser or request.user.is_admin:
        form = DiamondPiceBreakFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Maquina Compresora", "Equipo Perforador"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:diamond_pice_break_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, "tests_concrete/diamond_pice_break/diamond_pice_break_form.html", context)


@login_required
def diamond_pice_break_update(request, id):
    if request.user.is_bach or request.user.is_student:
        obj = get_object_or_404(DiamondPiceBreak, id=id)
        form = DiamondPiceBreakForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_concrete:diamond_pice_break_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(DiamondPiceBreak, id=id)
        form = DiamondPiceBreakFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_concrete:diamond_pice_break_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, "tests_concrete/diamond_pice_break/diamond_pice_break_form.html", context)


@login_required
def diamond_pice_break_detail(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)

    context = {
        "obj": obj,
        "title": "Detalles del Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_detail.html', context)


@login_required
def diamond_pice_break_delete(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)
    equips = Equip.objects.filter(name__in=("Maquina Compresora", "Equipo Perforador"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_concrete:diamond_pice_break_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo de Rotura de Testigos Diamantinos",
    }

    return render(request, 'tests_concrete/diamond_pice_break/diamond_pice_break_delete_comfirm.html', context)


# @login_required
# def diamond_pice_break_pdf(request, id):
#     obj = get_object_or_404(DiamondPiceBreak, id=id)

#     context = {
#         "obj": obj,
#     }

#     template = get_template('tests_concrete/diamond_pice_break/diamond_pice_break_pdf.html')
#     html = template.render(context)
#     options = {
#         'page-size': 'Letter',
#         'margin-top': '0.50in',
#         'margin-right': '0.50in',
#         'margin-bottom': '0.50in',
#         'margin-left': '0.50in',
#         'encoding': "UTF-8",
#     }
#     pdf = pdfkit.from_string(html, False, options)
#     response = HttpResponse(pdf, content_type='application/pdf')
#     # filename = str(obj.user.username) + str(id) + '.pdf'
#     filename = f"Ensayo_{obj.user.username}_{obj.id}.pdf"
#     response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
#     return response


@login_required
def diamond_pice_break_pdf(request, id):
    obj = get_object_or_404(DiamondPiceBreak, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first() 

    html = render_to_string('tests_concrete/diamond_pice_break/diamond_pice_break_pdf.html', {
        "obj": obj,
        "title": "CONCRETO. MÉTODO DE ENSAYO NORMALIZADO PARA LA DETERMINACIÓN DE LA RESISTENCIA A LA COMPRESIÓN DE TESTIGOS DIAMANTINOS EN MUESTRAS CILINDRICAS.",
        "norma_ASTM": "NORMA ASTM C-109",
        "noma_NTP": "NTP 334.034",
        "coordinator": coordinator,
        "tecnic": tecnic,
    })
    filename = f"Ensayo_{obj.user.username}_{obj.id}.pdf"
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)

    HTML(string=html).write_pdf(response)
    return response
