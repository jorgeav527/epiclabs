from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
import pdfkit
from django.template.loader import get_template
from django.db.models import F
from django.contrib.auth.decorators import login_required

from tests_concrete.models import PiceBreak
from tests_concrete.forms import PiceBreakForm, PiceBreakFormClient
from equipments.models import Equip

# Create your views here.

@login_required
def pice_break_list_view(request):
    if request.user.is_bach or request.user.is_student:
        obj_list = PiceBreak.objects.filter(user=request.user)
        context = {
            "file_name": "Testigos_de_Concreto",
            "title": "Ensayo de Rotura de Testigos de Concreto 6\" 4\" y 2\" ",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/pice_break/pice_break_list.html', context)        
    elif request.user.is_superuser or request.user.is_admin:
        obj_list = PiceBreak.objects.all()
        context = {
            "file_name": "Testigos_de_Concreto",
            "title": "Ensayo de Rotura de Testigos de Concreto 6\" 4\" y 2\" ",
            "obj_list": obj_list,
        }
        return render(request, 'tests_concrete/pice_break/pice_break_list.html', context)        


@login_required
def pice_break_create(request):
    if request.user.is_bach or request.user.is_student:
        form = PiceBreakForm(request.POST or None)
        equip = Equip.objects.get(name="Maquina Compresora")
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                form.instance.equipment.add(equip)
                equip.use = F("use") + 1 # equip.use += 1
                equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:pice_break_list')
    elif request.user.is_superuser or request.user.is_admin:
        form = PiceBreakFormClient(request.POST or None)
        equip = Equip.objects.get(name="Maquina Compresora")
        if request.method == "POST":
            if form.is_valid():
                form.save()
                form.instance.equipment.add(equip)
                equip.use = F("use") + 1 # equip.use += 1
                equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_concrete:pice_break_list')


    context = {
        "form": form
    }

    return render(request, "tests_concrete/pice_break/pice_break_form.html", context)


@login_required
def pice_break_update(request, id):
    obj = get_object_or_404(PiceBreak, id=id)
    form = PiceBreakForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"El ensayo ha sido actualizado")
            return redirect('tests_concrete:pice_break_list')

    context = {
        "form": form,
        "obj": obj,
    }

    return render(request, "tests_concrete/pice_break/pice_break_form.html", context)


@login_required
def pice_break_detail(request, id):
    obj = get_object_or_404(PiceBreak, id=id)

    context = {
        "obj": obj,
        "title": "Ensayo de Rotura de Testigos de Concreto",
    }

    return render(request, 'tests_concrete/pice_break/pice_break_detail.html', context)


@login_required
def pice_break_delete(request, id):
    obj = get_object_or_404(PiceBreak, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_concrete:pice_break_list')

    context = {
        "obj": obj,
    }

    return render(request, 'tests_concrete/pice_break/pice_break_delete_comfirm.html', context)


@login_required
def pice_break_pdf(request, id):
    obj = get_object_or_404(PiceBreak, id=id)

    context = {
        "obj": obj,
    }

    template = get_template('tests_concrete/pice_break/pice_break_pdf.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.50in',
        'margin-bottom': '0.75in',
        'margin-left': '0.50in',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filepdf.pdf"'
    return response