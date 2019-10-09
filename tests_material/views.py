from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
import pdfkit
from django.template.loader import get_template
from django.db.models import F

from .models import GroutDiceBreak
from .forms import GroutDiceBreakForm
from equipments.models import Equip

# Create your views here.

def tests_materials_info_view(request):
    context = {
        "title": "jojojo",
    }
    return render(request, 'tests_material/info.html', context)


def grout_dice_break_list_view(request):
    # file_name = "rotura_dados_concreto"
    object_list = GroutDiceBreak.objects.filter(user=request.user)
    # object_list = get_list_or_404(GroutDiceBreak.objects.filter(user=request.user))
    context = {
        "object_list": object_list,
        # "file_name": file_name,
    }
    return render(request, 'tests_material/grout_dice_break_list.html', context)


def grout_dice_break_create(request):
    form = GroutDiceBreakForm(request.POST or None)
    equip = Equip.objects.get(name="Maquina Compresora")
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            form.instance.equipment.add(equip)
            equip.use = F("use") + 1 # equip.use += 1
            equip.save()
            name = form.cleaned_data.get("name")
            user = form.cleaned_data.get("user")
            fecha_rotura = form.cleaned_data.get("fecha_rotura")
            messages.success(request, f"El ensayo de { name } por { user } { fecha_rotura } ha sido creado")
            return redirect('tests_material:dice_break_list')

    context = {
        "form": form
    }

    return render(request, "tests_material/grout_dice_brake_form.html", context)


def grout_dice_brake_update(request, id):
    obj = get_object_or_404(GroutDiceBreak, id=id)
    form = GroutDiceBreakForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            name = form.cleaned_data.get("name")
            user = form.cleaned_data.get("user")
            fecha_rotura = form.cleaned_data.get("fecha_rotura")
            messages.success(request, f"El ensayo de { name } por { user } { fecha_rotura } ha sido actualizado")
            return redirect('tests_material:dice_break_list')

    context = {
        "form": form,
        "obj": obj,
    }

    return render(request, "tests_material/grout_dice_brake_form.html", context)


def grout_dice_brake_delete(request, id):
    obj = get_object_or_404(GroutDiceBreak, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_material:dice_break_list')

    context = {
        "obj": obj,
    }

    return render(request, 'tests_material/grout_dice_brake_delete.html', context)


def grout_dice_brake_detail(request, id):
    obj = get_object_or_404(GroutDiceBreak, id=id)

    context = {
        "obj": obj,
    }

    return render(request, 'tests_material/grout_dice_brake_detail.html', context)


def grout_dice_brake_pdf(request, id):
    obj = get_object_or_404(GroutDiceBreak, id=id)

    context = {
        "obj": obj,
    }

    template = get_template('tests_material/grout_dice_brake_pdf.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="qwer.pdf"'
    return response



