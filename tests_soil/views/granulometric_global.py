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

from tests_soil.models import GranulometricGlobal, GlobalMesh
from tests_soil.forms import GranulometricGlobalForm, GranulometricGlobalFormClient, GlobalMeshFormSet
from equipments.models import Equip
from accounts.models import AdminProfile

# Classification SUCS.
name_0 = ""
name_1 = ""
name_2 = ""
name_3 = ""
name_4 = ""
def sucs(pass_200, pass_4, CU, CC, LL, IP):
    global name_0, name_1, name_2, name_3, name_4
    if pass_200 >= 50:
        name_0 = "Suelo Fino"
        if LL <= 50 and LL > 0:
            name_3 = "L"
        elif LL > 50 and LL <= 110:
            name_3 = "H"
        else:
            name_3 = "Verifique el Limite Liquido"
        if IP < 0.73 * (LL - 20):
            name_4 = "M"
        else: 
            name_4 = "C"
    elif pass_200 < 50:
        name_0 = "Suelo Grueso"
        if pass_4 >= 50:
            name_1 = "S"
            if pass_200 < 5:
                if CU > 6 and CC >=1 and CC <=3:
                    name_2 = "W"
                else:
                    name_2 = "P" 
            elif pass_200 >= 5 and pass_200 <= 12:
                if CU > 6 and CC >=1 and CC <=3:
                    name_2 = "W"
                else:
                    name_2 = "P"
                if LL <= 50 and LL > 0:
                    name_3 = "L"
                elif LL > 50 and LL <= 110:
                    name_3 = "H"
                else:
                    name_3 = "Verifique el Limite Liquido"
                if IP < 0.73 * (LL - 20):
                    name_4 = "M"
                else: 
                    name_4 = "C"
            elif pass_200 > 12:
                if IP < 0.73 * (LL - 20):
                    name_4 = "M"
                else: 
                    name_4 = "C"
        elif pass_4 < 50:
            name_1 = "G"
            if pass_200 < 5:
                if CU > 6 and CC >=1 and CC <=3:
                    name_2 = "W"
                else:
                    name_2 = "P" 
            elif pass_200 >= 5 and pass_200 <= 12:
                if CU > 6 and CC >=1 and CC <=3:
                    name_2 = "W"
                else:
                    name_2 = "P"
                if LL <= 50 and LL > 0:
                    name_3 = "L"
                elif LL > 50 and LL <= 110:
                    name_3 = "H"
                else:
                    name_3 = "Verifique el Limite Liquido"
                if IP < 0.73 * (LL - 20):
                    name_4 = "M"
                else: 
                    name_4 = "C"
            elif pass_200 > 12:
                if IP < 0.73 * (LL - 20):
                    name_4 = "M"
                else: 
                    name_4 = "C"
    
    return name_0, name_1, name_2, name_3, name_4


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
def global_mesh_save(request, id):
    obj = get_object_or_404(GranulometricGlobal, id=id)
    equips = Equip.objects.filter(name__in=("Tamizadora", "Balanza",))
    if request.user.is_bach or request.user.is_group or request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            formset = GlobalMeshFormSet(request.POST, instance=obj)
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
                return redirect('tests_soil:global_mesh_save', id=obj.id)
    
    formset = GlobalMeshFormSet(instance=obj)

    context = {
        "obj": obj,
        "formset": formset,
        "title": "Crear Ensayo de Granulometria Gloval",
    }

    return render(request, "tests_soil/granulometric_global/global_mesh_form.html", context)


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
    tamiz = GlobalMesh.objects.filter(granulometric_global=obj.id).first()

    granulometric = [
        {    
            'id': 1,   
            'mesh': '4"',
            'retained': tamiz.tamiz_4,
            'diamether': 101.6,
        },
        {    
            'id': 2,
            'mesh': '3"',
            'retained': tamiz.tamiz_3,
            'diamether': 76.2,
        },
        {    
            'id': 3,
            'mesh': '2 1/2"',
            'retained': tamiz.tamiz_2_1o2,
            'diamether': 63.5,
        },
        {    
            'id': 4,
            'mesh': '2"',
            'retained': tamiz.tamiz_2,
            'diamether': 50.8,
        },
        {    
            'id': 5,
            'mesh': '1 1/2"',
            'retained': tamiz.tamiz_1_1o2,
            'diamether': 38.1,
        },
        {   
            'id': 6,
            'mesh': '1"',
            'retained': tamiz.tamiz_1,
            'diamether': 25.4,
        },
        {   
            'id': 7,
            'mesh': '3/4"',
            'retained': tamiz.tamiz_3o4,
            'diamether': 19.05,
        },
        {   
            'id': 8,
            'mesh': '1/2"',
            'retained': tamiz.tamiz_1o2,
            'diamether': 12.7,
        },
        {   
            'id': 9,
            'mesh': '3/8"',
            'retained': tamiz.tamiz_3o8,
            'diamether': 9.5,
        },
        {   
            'id': 10,
            'mesh': '# 4',
            'retained': tamiz.tamiz_N_4,
            'diamether': 4.75,
        },
        {   
            'id': 11,
            'mesh': '# 8',
            'retained': tamiz.tamiz_N_8,
            'diamether': 2.36,
        },
        {   
            'id': 12,
            'mesh': '# 10',
            'retained': tamiz.tamiz_N_10,
            'diamether': 2.0,
        },
        {   
            'id': 13,
            'mesh': '# 16',
            'retained': tamiz.tamiz_N_16,
            'diamether': 1.18,
        },
        {   
            'id': 14,
            'mesh': '# 20',
            'retained': tamiz.tamiz_N_20,
            'diamether': 0.85,
        },
        {   
            'id': 15,
            'mesh': '# 30',
            'retained': tamiz.tamiz_N_30,
            'diamether': 0.6,
        },
        {   
            'id': 16,
            'mesh': '# 40',
            'retained': tamiz.tamiz_N_40,
            'diamether': 0.425,
        },
        {   
            'id': 17,
            'mesh': '# 50',
            'retained': tamiz.tamiz_N_50,
            'diamether': 0.3,
        },
        {   
            'id': 18,
            'mesh': '# 60',
            'retained': tamiz.tamiz_N_60,
            'diamether': 0.25,
        },
        {   
            'id': 19,
            'mesh': '# 80',
            'retained': tamiz.tamiz_N_80,
            'diamether': 0.18,
        },
        {   
            'id': 20,
            'mesh': '# 100',
            'retained': tamiz.tamiz_N_100,
            'diamether': 0.15,
        },
        {   
            'id': 21,
            'mesh': '# 140',
            'retained': tamiz.tamiz_N_140,
            'diamether': 0.106,
        },
        {   
            'id': 22,
            'mesh': '# 200',
            'retained': tamiz.tamiz_N_200,
            'diamether': 0.075,
        },
        {   
            'id': 23,
            'mesh': 'Fondo',
            'retained': tamiz.tamiz_fondo,
            'diamether': 0.065,
        },
    ]

    retained_weight = []
    name_mesh = []
    diameter_mesh = []

    used_mesh = filter(lambda item: item['retained'] is not None, granulometric)
    for i in used_mesh:
        retained_weight.append(i['retained'])
        name_mesh.append(i['mesh'])
        diameter_mesh.append(i['diamether'])

    total_amount = 0

    for i in range(len(retained_weight)):
        total_amount = round(total_amount + retained_weight[i], 1)

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

    gravas = []
    used_gravas = filter(lambda item: item['retained'] is not None and item['id'] <= 10, granulometric)
    for i in used_gravas:
        gravas.append(i['retained'])
    
    total_gravas = round(sum(gravas) / total_amount * 100, 2)
        
    arenas = []
    used_arenas = filter(lambda item: item['retained'] is not None and item['id'] > 10 and item['id'] < 23, granulometric)
    for i in used_arenas:
        arenas.append(i['retained'])
    
    total_arenas = round(sum(arenas) / total_amount * 100, 2)

    finos = []
    used_finos = filter(lambda item: item['retained'] is not None and item['id'] == 23, granulometric)
    for i in used_finos:
        finos.append(i['retained'])
    
    total_finos = round(sum(finos) / total_amount * 100, 2)

    if total_finos <= 10:
        d_x = []
        decil = [60, 30, 10]
        position = []
        for i in (0,1,2):
            for k in range(0, len(passing_percentage)):
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

    if obj.max_size == '# 4' and total_amount >= 100:
        min_total_amount = "Ok"
    elif obj.max_size == '3/8"' or  obj.max_size == '1/2"' and total_amount >= 200:
        min_total_amount = "Ok"
    elif obj.max_size == '3/4"' or obj.max_size == '1"' and total_amount >= 1: 
        min_total_amount = "Ok"
    elif obj.max_size == '1 1/2"' or obj.max_size == '2"' or obj.max_size == '2 1/2"' and total_amount >= 8: 
        min_total_amount = "Ok"
    elif obj.max_size == '3"' or obj.max_size == '4"' and total_amount >= 60: 
        min_total_amount = "Ok"
    else:
        min_total_amount = "Verifique el Peso Seco Mínimo"
    
    # SUCS
    used = []
    used_4_200 = filter(lambda item: item['retained'] is not None, granulometric)
    for i in used_4_200:
        used.append(i['id'])

    pass_4 = passing_percentage[used.index(10)]
    pass_200 = passing_percentage[used.index(22)]

    names = sucs(pass_200, pass_4, CU, CC, obj.liquid_limit, obj.plastic_index)
    name_sucs_fino_grueso = names[0]
    name_sucs_S_G = names[1]
    name_sucs_W_P = names[2]
    name_sucs_L_H = names[3]
    name_sucs_M_C = names[4]

    # ASSTHO

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
        "total_gravas": total_gravas,
        "total_finos": total_finos,
        "total_arenas": total_arenas,
        "decil_60": decil_60,
        "decil_30": decil_30,
        "decil_10": decil_10,
        "CU": CU,
        "CC": CC,
        "min_total_amount": min_total_amount,
        "name_sucs_fino_grueso": name_sucs_fino_grueso,
        "name_sucs_S_G": name_sucs_S_G,
        "name_sucs_W_P": name_sucs_W_P,
        "name_sucs_L_H": name_sucs_L_H,
        "name_sucs_M_C": name_sucs_M_C,
        "norma_ASTM": "",
        "noma_NTP": "NPT 339.134",
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

    tamiz = GlobalMesh.objects.filter(granulometric_global=obj.id).first()

    granulometric = [
        {    
            'id': 1,   
            'mesh': '4"',
            'retained': tamiz.tamiz_4,
            'diamether': 101.6,
        },
        {    
            'id': 2,
            'mesh': '3"',
            'retained': tamiz.tamiz_3,
            'diamether': 76.2,
        },
        {    
            'id': 3,
            'mesh': '2 1/2"',
            'retained': tamiz.tamiz_2_1o2,
            'diamether': 63.5,
        },
        {    
            'id': 4,
            'mesh': '2"',
            'retained': tamiz.tamiz_2,
            'diamether': 50.8,
        },
        {    
            'id': 5,
            'mesh': '1 1/2"',
            'retained': tamiz.tamiz_1_1o2,
            'diamether': 38.1,
        },
        {   
            'id': 6,
            'mesh': '1"',
            'retained': tamiz.tamiz_1,
            'diamether': 25.4,
        },
        {   
            'id': 7,
            'mesh': '3/4"',
            'retained': tamiz.tamiz_3o4,
            'diamether': 19.05,
        },
        {   
            'id': 8,
            'mesh': '1/2"',
            'retained': tamiz.tamiz_1o2,
            'diamether': 12.7,
        },
        {   
            'id': 9,
            'mesh': '3/8"',
            'retained': tamiz.tamiz_3o8,
            'diamether': 9.5,
        },
        {   
            'id': 10,
            'mesh': '# 4',
            'retained': tamiz.tamiz_N_4,
            'diamether': 4.75,
        },
        {   
            'id': 11,
            'mesh': '# 8',
            'retained': tamiz.tamiz_N_8,
            'diamether': 2.36,
        },
        {   
            'id': 12,
            'mesh': '# 10',
            'retained': tamiz.tamiz_N_10,
            'diamether': 2.0,
        },
        {   
            'id': 13,
            'mesh': '# 16',
            'retained': tamiz.tamiz_N_16,
            'diamether': 1.18,
        },
        {   
            'id': 14,
            'mesh': '# 20',
            'retained': tamiz.tamiz_N_20,
            'diamether': 0.85,
        },
        {   
            'id': 15,
            'mesh': '# 30',
            'retained': tamiz.tamiz_N_30,
            'diamether': 0.6,
        },
        {   
            'id': 16,
            'mesh': '# 40',
            'retained': tamiz.tamiz_N_40,
            'diamether': 0.425,
        },
        {   
            'id': 17,
            'mesh': '# 50',
            'retained': tamiz.tamiz_N_50,
            'diamether': 0.3,
        },
        {   
            'id': 18,
            'mesh': '# 60',
            'retained': tamiz.tamiz_N_60,
            'diamether': 0.25,
        },
        {   
            'id': 19,
            'mesh': '# 80',
            'retained': tamiz.tamiz_N_80,
            'diamether': 0.18,
        },
        {   
            'id': 20,
            'mesh': '# 100',
            'retained': tamiz.tamiz_N_100,
            'diamether': 0.15,
        },
        {   
            'id': 21,
            'mesh': '# 140',
            'retained': tamiz.tamiz_N_140,
            'diamether': 0.106,
        },
        {   
            'id': 22,
            'mesh': '# 200',
            'retained': tamiz.tamiz_N_200,
            'diamether': 0.075,
        },
        {   
            'id': 23,
            'mesh': 'Fondo',
            'retained': tamiz.tamiz_fondo,
            'diamether': 0.065,
        },
    ]

    retained_weight = []
    name_mesh = []
    diameter_mesh = []

    used_mesh = filter(lambda item: item['retained'] is not None, granulometric)
    for i in used_mesh:
        retained_weight.append(i['retained'])
        name_mesh.append(i['mesh'])
        diameter_mesh.append(i['diamether'])

    total_amount = 0

    for i in range(len(retained_weight)):
        total_amount = round(total_amount + retained_weight[i], 1)

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

    gravas = []
    used_gravas = filter(lambda item: item['retained'] is not None and item['id'] <= 10, granulometric)
    for i in used_gravas:
        gravas.append(i['retained'])
    
    total_gravas = round(sum(gravas) / total_amount * 100, 2)
        
    arenas = []
    used_arenas = filter(lambda item: item['retained'] is not None and item['id'] > 10 and item['id'] < 23, granulometric)
    for i in used_arenas:
        arenas.append(i['retained'])
    
    total_arenas = round(sum(arenas) / total_amount * 100, 2)

    finos = []
    used_finos = filter(lambda item: item['retained'] is not None and item['id'] == 23, granulometric)
    for i in used_finos:
        finos.append(i['retained'])
    
    total_finos = round(sum(finos) / total_amount * 100, 2)

    if total_finos <= 10:
        d_x = []
        decil = [60, 30, 10]
        position = []
        for i in (0,1,2):
            for k in range(0, len(passing_percentage)):
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

    if obj.max_size == '# 4' and total_amount >= 100:
        min_total_amount = "Ok"
    elif obj.max_size == '3/8"' or  obj.max_size == '1/2"' and total_amount >= 200:
        min_total_amount = "Ok"
    elif obj.max_size == '3/4"' or obj.max_size == '1"' and total_amount >= 1: 
        min_total_amount = "Ok"
    elif obj.max_size == '1 1/2"' or obj.max_size == '2"' or obj.max_size == '2 1/2"' and total_amount >= 8: 
        min_total_amount = "Ok"
    elif obj.max_size == '3"' or obj.max_size == '4"' and total_amount >= 60: 
        min_total_amount = "Ok"
    else:
        min_total_amount = "Verifique el Peso Seco Mínimo"
    
    # SUCS
    used = []
    used_4_200 = filter(lambda item: item['retained'] is not None, granulometric)
    for i in used_4_200:
        used.append(i['id'])

    pass_4 = passing_percentage[used.index(10)]
    pass_200 = passing_percentage[used.index(22)]

    names = sucs(pass_200, pass_4, CU, CC, obj.liquid_limit, obj.plastic_index)
    name_sucs_fino_grueso = names[0]
    name_sucs_S_G = names[1]
    name_sucs_W_P = names[2]
    name_sucs_L_H = names[3]
    name_sucs_M_C = names[4]

    # ASSTHO

    # Ploting
    max_x = np.max(diameter_mesh)
    min_x = np.min(diameter_mesh)
    max_y = np.max(passing_percentage)
    min_y = np.min(passing_percentage)

    fig = plt.figure(figsize=(6.4, 5.5), dpi=80)

    plt.xlim(max_x, min_x)
    plt.ylim(min_y, max_y)
    plt.xscale('log')
    plt.grid(b=True, which='both', axis='both')

    plt.scatter(diameter_mesh, passing_percentage, label='Resultados', s=20, c='blue',)
    plt.plot(diameter_mesh, passing_percentage, color='green', linestyle='dashed',)
    plt.scatter(decil_60, decil[0], label='Decil 60', marker="x", s=20, c='c',)
    plt.scatter(decil_30, decil[1], label='Decil 30', marker="x", s=20, c='m',)
    plt.scatter(decil_10, decil[2], label='Decil 10', marker="x", s=20, c='y',)

    plt.xlabel('Diametro de la Malla (mm)')
    plt.ylabel('Porcentaje Pasante (%)')
    plt.title("Curva Granulometrica")
    plt.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    graphic = base64.b64encode(buf.getbuffer()).decode("ascii")

    context = {
        "obj": obj,
        "retained_weight": retained_weight,
        "name_mesh": name_mesh,
        "diameter_mesh": diameter_mesh,
        "total_amount": total_amount,
        "percentage_retained": percentage_retained,
        "retained_accumulated": retained_accumulated,
        "passing_percentage": passing_percentage,
        "total_gravas": total_gravas,
        "total_finos": total_finos,
        "total_arenas": total_arenas,
        "decil_60": decil_60,
        "decil_30": decil_30,
        "decil_10": decil_10,
        "CU": CU,
        "CC": CC,
        "min_total_amount": min_total_amount,
        "name_sucs_fino_grueso": name_sucs_fino_grueso,
        "name_sucs_S_G": name_sucs_S_G,
        "name_sucs_W_P": name_sucs_W_P,
        "name_sucs_L_H": name_sucs_L_H,
        "name_sucs_M_C": name_sucs_M_C,
        "graphic": graphic,
        "title": "CLASIFICACIÓN DE SUELOS PARA FINES DE INGENIERÍA Y CONSTRUCCIÓN DE CARRETERAS",
        "norma_ASTM": "",
        "noma_NTP": "NPT 339.134",
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
