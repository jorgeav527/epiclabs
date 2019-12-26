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
from PIL import Image

from tests_soil.models import GranulometricGlobal
from tests_soil.forms import GranulometricGlobalForm, GranulometricGlobalFormClient
from equipments.models import Equip
from accounts.models import AdminProfile


# Create your views here.

@login_required
def granulometric_global_list(request):

    if request.user.is_bach or request.user.is_group or request.user.is_client:
        obj_list = GranulometricGlobal.objects.filter(user=request.user)
        context = {
            "file_name": "Granulometria_Gloval",
            "title": "Ensayos de Granulometria Gloval",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/granulometric_global/granulometric_global_list.html', context) 

    elif request.user.is_superuser or request.user.is_admin:
        obj_list = GranulometricGlobal.objects.all()
        context = {
            "file_name": "Granulometria_Gloval",
            "title": "Ensayos de Granulometria Gloval",
            "obj_list": obj_list,
        }
        return render(request, 'tests_soil/granulometric_global/granulometric_global_list.html', context)        


@login_required
def granulometric_global_create(request):

    if request.user.is_bach or request.user.is_group:
        form = GranulometricGlobalForm(request.POST or None)
        equips = Equip.objects.filter(name__in=("Tamizadora", "Balanza"))
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:granulometric_global_list')

    elif request.user.is_superuser or request.user.is_admin:
        form = GranulometricGlobalFormClient(request.POST or None)
        equips = Equip.objects.filter(name__in=("Tamizadora", "Balanza"))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                for equip in equips:
                    form.instance.equipment.add(equip)
                    equip.use = F("use") + 1
                    equip.save()
                messages.success(request, f"El ensayo ha sido creado")
                return redirect('tests_soil:granulometric_global_list')

    context = {
        "form": form,
        "title": "Crear Ensayo de Granulometria Gloval",
    }

    return render(request, "tests_soil/granulometric_global/granulometric_global_form.html", context)


@login_required
def granulometric_global_update(request, id):

    if request.user.is_bach or request.user.is_group:
        obj = get_object_or_404(GranulometricGlobal, id=id)
        form = GranulometricGlobalForm(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:granulometric_global_list')

    elif request.user.is_superuser or request.user.is_admin:
        obj = get_object_or_404(GranulometricGlobal, id=id)
        form = GranulometricGlobalFormClient(request.POST or None, instance=obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"El ensayo ha sido actualizado")
                return redirect('tests_soil:granulometric_global_list')

    context = {
        "form": form,
        "obj": obj,
        "title": "Actualizar Ensayo de Granulometria Gloval",
    }

    return render(request, "tests_soil/granulometric_global/granulometric_global_form.html", context)


@login_required
def granulometric_global_detail(request, id):
    obj = get_object_or_404(GranulometricGlobal, id=id)
    retained_weight = [
        obj.tamiz_1_1o2, obj.tamiz_1, obj.tamiz_3o4, obj.tamiz_1o2, obj.tamiz_3o8, 
        obj.tamiz_4, obj.tamiz_10, obj.tamiz_20, obj.tamiz_40, obj.tamiz_60, obj.tamiz_100, obj.tamiz_200, obj.tamiz_fondo,
    ]
    name_mesh = ['1 1/2"', '1"', '3/4"', '1/2"', '3/8"', '# 4', '# 10', '# 20', '# 40', '# 60', '# 100', '# 200', 'fondo',]
    diameter_mesh = [38.100, 25.400, 19.050, 12.700, 9.500, 4.750, 2.000, 0.850, 0.425, 0.250, 0.150, 0.075, 0.065]

    total_amount = 0

    for i in range(len(retained_weight)):
        total_amount = total_amount + retained_weight[i]

    percentage_retained = []

    for i in range(len(retained_weight)):
        ret_p = round(retained_weight[i]/total_amount * 100, 2) 
        percentage_retained.append(ret_p)

    retained_accumulated = []
    retained_accumulated.append(percentage_retained[0])

    for i in range(1, len(retained_weight)):
        ret_a = round(retained_accumulated[i-1] + percentage_retained[i], 2) 
        retained_accumulated.append(ret_a)

    passing_percentage = []
    passing_percentage.append(100 - retained_accumulated[0])

    for i in range(1, len(retained_weight)):
        pass_p = round(100 - retained_accumulated[i], 2) 
        passing_percentage.append(pass_p)

    gravas = round(100 - passing_percentage[len(retained_weight) - 8], 2)
    finos = round(passing_percentage[len(retained_weight) - 2], 2)
    arenas = round(100 - gravas - finos, 2)

    if finos <= 10:
        d_x = []
        decil = [60, 30, 10]
        position = []
        for i in (0,1,2):
            for k in range(0,13):
                if passing_percentage[k] <= decil[i]:
                    position.append(k)
                    break # 7, 9, 10
            a = (passing_percentage[position[i]-1]-decil[i])
            b = diameter_mesh[position[i]-1] - diameter_mesh[position[i]] 
            c = passing_percentage[position[i] - 1] - passing_percentage[position[i]]
            d = round(diameter_mesh[position[i] - 1] - (b * a / c), 2)
            d_x.append(d)
        
        decil_60 = d_x[0]
        decil_30 = d_x[1]
        decil_10 = d_x[2]
        CU = round(decil_60  / decil_10, 2)
        CC = round((decil_30 ** 2) / (decil_10 * decil_60 ), 2)

    # Ploting
    max_x = np.max(diameter_mesh)
    min_x = np.min(diameter_mesh)
    max_y = np.max(passing_percentage)
    min_y = np.min(passing_percentage)

    TOOLS="hover,crosshair,pan,wheel_zoom,reset,save,"
    plot = figure(x_axis_type="log", x_range=(max_x, min_x), y_range=(min_y, max_y), tools=TOOLS, 
        title="Curva Granulometrica", x_axis_label= 'Diametro de la Malla (mm)', y_axis_label= 'Porcentaje Pasante (%)',
        sizing_mode="scale_width",)
    plot.circle(diameter_mesh, passing_percentage, size=8, legend="Resultados")
    plot.line(diameter_mesh, passing_percentage, line_width=2, line_dash='dashed')
    plot.circle(d_x, decil, size=8, color="red", legend="Deciles")
    script, div = components(plot)

    context = {
        "script": script,
        "div": div,
        "obj": obj,
        "retained_weight": retained_weight,
        "name_mesh": name_mesh,
        "diameter_mesh": diameter_mesh,
        "total_amount": total_amount,
        "percentage_retained": percentage_retained,
        "retained_accumulated": retained_accumulated,
        "passing_percentage": passing_percentage,
        "gravas": gravas,
        "finos": finos,
        "arenas": arenas,
        "decil_60": decil_60,
        "decil_30": decil_30,
        "decil_10": decil_10,
        "CU": CU,
        "CC": CC,
        "norma_ASTM": "ASTM D1140",
        "noma_NTP": "ASTM D3282",
        "title": "Detalles del Ensayo Granulometria Gloval",
    }

    return render(request, 'tests_soil/granulometric_global/granulometric_global_detail.html', context)


@login_required
def granulometric_global_delete(request, id):
    obj = get_object_or_404(GranulometricGlobal, id=id)
    equips = Equip.objects.filter(name__in=("Tamizadora", "Balanza"))
    if request.method == "POST":
        obj.delete()
        for equip in equips:
            equip.use = F("use") - 1 # equip.use += 1
            equip.save()
        messages.success(request, f"El ensayo a sido eliminado")
        return redirect('tests_soil:granulometric_global_list')

    context = {
        "obj": obj,
        "title": "Eliminar el Ensayo Granulometria Gloval",
    }

    return render(request, 'tests_soil/granulometric_global/granulometric_global_delete_comfirm.html', context)


@login_required
def granulometric_global_pdf(request, id):
    obj = get_object_or_404(GranulometricGlobal, id=id)
    coordinator = AdminProfile.objects.filter(staff="COORDINADOR", active=True).first() 
    tecnic = AdminProfile.objects.filter(staff="OFICINA_TECNICA", active=True).first() 
    retained_weight = [
        obj.tamiz_1_1o2, obj.tamiz_1, obj.tamiz_3o4, obj.tamiz_1o2, obj.tamiz_3o8, 
        obj.tamiz_4, obj.tamiz_10, obj.tamiz_20, obj.tamiz_40, obj.tamiz_60, obj.tamiz_100, obj.tamiz_200, obj.tamiz_fondo,
    ]
    name_mesh = ['1 1/2"', '1"', '3/4"', '1/2"', '3/8"', '# 4', '# 10', '# 20', '# 40', '# 60', '# 100', '# 200', 'fondo',]
    diameter_mesh = [38.100, 25.400, 19.050, 12.700, 9.500, 4.750, 2.000, 0.850, 0.425, 0.250, 0.150, 0.075, 0.065]

    total_amount = 0

    for i in range(len(retained_weight)):
        total_amount = total_amount + retained_weight[i]

    percentage_retained = []

    for i in range(len(retained_weight)):
        ret_p = round(retained_weight[i]/total_amount * 100, 2) 
        percentage_retained.append(ret_p)

    retained_accumulated = []
    retained_accumulated.append(percentage_retained[0])

    for i in range(1, len(retained_weight)):
        ret_a = round(retained_accumulated[i-1] + percentage_retained[i], 2) 
        retained_accumulated.append(ret_a)

    passing_percentage = []
    passing_percentage.append(100 - retained_accumulated[0])

    for i in range(1, len(retained_weight)):
        pass_p = round(100 - retained_accumulated[i], 2) 
        passing_percentage.append(pass_p)

    gravas = round(100 - passing_percentage[len(retained_weight) - 8], 2)
    finos = round(passing_percentage[len(retained_weight) - 2], 2)
    arenas = round(100 - gravas - finos, 2)

    if finos <= 10:
        d_x = []
        decil = [60, 30, 10]
        position = []
        for i in (0,1,2):
            for k in range(0,13):
                if passing_percentage[k] <= decil[i]:
                    position.append(k)
                    break # 7, 9, 10
            a = (passing_percentage[position[i]-1]-decil[i])
            b = diameter_mesh[position[i]-1] - diameter_mesh[position[i]] 
            c = passing_percentage[position[i] - 1] - passing_percentage[position[i]]
            d = round(diameter_mesh[position[i] - 1] - (b * a / c), 2)
            d_x.append(d)
        
        decil_60 = d_x[0]
        decil_30 = d_x[1]
        decil_10 = d_x[2]
        CU = round(decil_60  / decil_10, 2)
        CC = round((decil_30 ** 2) / (decil_10 * decil_60 ), 2)

    # Ploting
    fig = plt.figure()
    x = np.linspace(0, 2, 100)

    plt.plot(x, x, label='linear')
    plt.plot(x, x**2, label='quadratic')
    plt.plot(x, x**3, label='cubic')

    plt.xlabel('x label')
    plt.ylabel('y label')

    plt.title("Simple Plot")

    plt.legend()

    plt.tight_layout()

    canvas = fig.canvas
    buf, size = canvas.print_to_buffer()
    image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
    buffer = BytesIO()
    image.save(buffer,'PNG')
    graphic = buffer.getvalue()
    graphic = base64.b64encode(graphic)
    buffer.close()

    context = {
        "obj": obj,
        "retained_weight": retained_weight,
        "name_mesh": name_mesh,
        "diameter_mesh": diameter_mesh,
        "total_amount": total_amount,
        "percentage_retained": percentage_retained,
        "retained_accumulated": retained_accumulated,
        "passing_percentage": passing_percentage,
        "gravas": gravas,
        "finos": finos,
        "arenas": arenas,
        "decil_60": decil_60,
        "decil_30": decil_30,
        "decil_10": decil_10,
        "CU": CU,
        "CC": CC,
        "graphic": str(graphic)[2:-1],
        "title": "CLASIFICACIÓN DE SUELOS PARA FINES DE INGENIERÍA Y CONSTRUCCIÓN DE CARRETERAS",
        "norma_ASTM": "ASTM D2487",
        "noma_NTP": "ASTM D3282",
        "coordinator": coordinator,
        "tecnic": tecnic,
    }
    html = render_to_string('tests_soil/granulometric_global/granulometric_global_pdf.html', context)
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
