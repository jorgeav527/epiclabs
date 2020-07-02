from django.shortcuts import render

from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.plotting import figure
from bokeh.embed import components

from accounts.models import *
from equipments.models import *
from reference_person.models import *
from construction.models import *
from thesis.models import *
from students.models import *
from tests_concrete.models import *
from tests_material.models import *
from tests_soil.models import *

# GENERAL REUSE FUNCTIONS
#========================

def graph_general_tests(tests_clients, tests_bachs, tests_groups):
    x = {
        'Clientes': tests_clients,
        'Tesistas': tests_bachs,
        'Estudiantes': tests_groups,
    }

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'sectores'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]

    TOOLS="hover,pan,wheel_zoom,reset,save"
    plot = figure(plot_height=350, title="Cantidad de Ensayos vs Sectores",
        tools=TOOLS, tooltips="@sectores: @value", x_range=(-0.4, 0.7), 
        sizing_mode="fixed")

    plot.wedge(x=0, y=1, radius=0.3,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='sectores', source=data)

    plot.axis.axis_label=None
    plot.axis.visible=False
    plot.grid.grid_line_color = None
    script, div = components(plot)

    return script, div


# GENERAL VIEWS USERS
#====================

def general_view(request):
    return render(request, 'labs/sectors/general/general.html')


def general_clients_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_users = User.objects.filter(is_client=True)

    context = {
        "title": "Informacion de Clientes",
        "qs_users": qs_users,
    }
    return render(request, 'labs/sectors/general/info/general_clients.html', context)


def general_ref_per_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_ref_persons = ReferencePerson.objects.all()

    context = {
        "title": "Personas de Referencia de los Clientes",
        "qs_ref_persons": qs_ref_persons,
    }
    return render(request, 'labs/sectors/general/info/general_ref_per.html', context)


def general_construction_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_constructions = Construction.objects.all()

    context = {
        "title": "Proyectos de los Clientes",
        "qs_constructions": qs_constructions,
    }
    return render(request, 'labs/sectors/general/info/general_construction.html', context)


def general_personal_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_admins = User.objects.filter(is_admin=True)
        qs_teachers = User.objects.filter(is_teacher=True)

    context = {
        "title_admin": "Personal Administrativo",
        "title_teacher": "Personal Docente",
        "qs_admins": qs_admins,
        "qs_teachers": qs_teachers,
    }
    return render(request, 'labs/sectors/general/info/general_personal.html', context)


def general_bach_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_users = User.objects.filter(is_bach=True)

    context = {
        "title": "Información de los Tesistas",
        "qs_users": qs_users,
    }
    return render(request, 'labs/sectors/general/info/general_bach.html', context)


def general_thesis_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_thesis = Thesis.objects.all()

    context = {
        "title": "Información de las Tesis",
        "qs_thesis": qs_thesis,
    }
    return render(request, 'labs/sectors/general/info/general_thesis.html', context)


def general_student_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_users = User.objects.filter(is_group=True)
        qs_students = Student.objects.all()

    context = {
        "title_users": "Grupos y Responsables",
        "title_students": "Estudiantes de los Grupos",
        "qs_users": qs_users,
        "qs_students": qs_students,
    }
    return render(request, 'labs/sectors/general/info/general_student.html', context)


def general_equips_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_equips = Equip.objects.all()

    qs_equips_names = qs_equips.values_list("name", flat=True)
    qs_equips_uses = qs_equips.values_list("use", flat=True)

    x = dict(zip(qs_equips_names, qs_equips_uses))

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'equipos'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]

    TOOLS="hover,pan,wheel_zoom,reset,save"
    plot = figure(plot_height=500, title="Equipos vs Uso",
        tools=TOOLS, tooltips="@equipos: @value", x_range=(-0.4, 0.7), 
        sizing_mode="fixed")

    plot.wedge(x=0, y=1, radius=0.3,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='equipos', source=data)

    plot.axis.axis_label=None
    plot.axis.visible=False
    plot.grid.grid_line_color = None
    script, div = components(plot)

    context = {
        "script": script,
        "div": div,
        "title": "Personal",
        "qs_equips": qs_equips,
    }
    return render(request, 'labs/sectors/general/info/general_equips.html', context)


# GENERAL VIEWS TESTS CONCRETE
#=============================

def general_diamond_pice_break(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = DiamondPiceBreak.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "RESISTENCIA A LA COMPRESIÓN DE TESTIGOS DIAMANTINOS EN MUESTRAS CILINDRICAS",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_concrete/general_diamond_pice_break.html', context)


def general_pice_break(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = PiceBreak.objects.all()
    
    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINACIÓN DE LA RESISTENCIA A LA COMPRESIÓN DE TESTIGOS EN MUESTRAS CILINDRICAS",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_concrete/general_pice_break.html', context)


def general_prism_break(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = PrismBreak.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINACIÓN DE LA RESISTENCIA A LA COMPRESIÓN DE TESTIGOS EN MUESTRAS PRISMÁTICAS",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_concrete/general_prism_break.html', context)

# GENERAL VIEWS TESTS MATERIAL
#=============================

def general_brick_type(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = BrickType.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINAR LAS PROPIEDADES EN UNIDADES DE ALBAÑILERIA CALCINADA PARA LA CONSTRUCCIÓN",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_material/general_brick_type.html', context)


def general_masonry_compression(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = MasonryCompression.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINACIÓN DE LA RESISTENCIA EN COMPRESIÓN DE PRISMAS DE ALBAÑILERIA",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_material/general_masonry_compression.html', context)

def general_wood_compression(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = WoodCompression.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINAR LA COMPRESIÓN SIMPLE, PERPENDICULAR O PARALELA EN MADERA",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_material/general_wood_compression.html', context)

# GENERAL VIEWS TESTS SOIL
#=========================

def general_equivalent(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = Equivalent.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "ENSAYO ESTÁNDAR PARA EL VALOR EQUIVALENTE DE ARENA DE SUELOS Y AGREGADO FINO - MTC E114",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_equivalent.html', context)


def general_fine_material(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = FineMaterial.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINACIÓN DE MATERIAL MAS FINO QUE EL TAMIZ 75μm (Nro. 200) EN SUELOS MTC E137",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_fine_material.html', context)


def general_granulometric_global(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = GranulometricGlobal.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "CLASIFICACIÓN DE SUELOS PARA FINES DE INGENIERÍA Y CONSTRUCCIÓN DE CARRETERAS",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_granulometric_global.html', context)


def general_limit(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = Limit.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINAR EL LIMITE LÍQUIDO, LIMITE PLÁSTICO E INDICE DE PLASTICIDAD DE SUELOS MTC E110 - MTC E111",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_limit.html', context)


def general_moisture_content(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = MoistureContent.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINACIÓN DEL CONTENIDO DE HUMEDAD DE UN SUELO MTC E108",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_moisture_content.html', context)


def general_proctor_m(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = ProctorM.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "COMPACTACION DE SUELOS EN LABORATORIO UTILIZANDO UNA ENERGIA MODIFICADA (2 700 kN-m/m³ (56 000 pie-lbf/pie³)) PROCTOR MODIFICADO MTC E115",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_proctor_m.html', context)


def general_sand_cone(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = SandCone.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "ENSAYO PARA DETERMINAR LA DENSIDAD Y PESO UNITARIO DEL SUELO IN SITU MEDIANTE EL MÉTODO DEL CONO DE ARENA - MTC E117",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_sand_cone.html', context)


def general_specific_gravity(request):
    if request.user.is_superuser or request.user.is_admin:
        qs = SpecificGravity.objects.all()

    tests_clients   = qs.filter(user__is_client=True).count()
    tests_bachs     = qs.filter(user__is_bach=True).count()
    tests_groups    = qs.filter(user__is_group=True).count()

    graph = graph_general_tests(tests_clients, tests_bachs, tests_groups)
    script = graph[0]
    div = graph[1]

    context = {
        "script": script,
        "div": div,
        "tests_clients": tests_clients,
        "tests_bachs": tests_bachs,
        "tests_groups": tests_groups,
        "title": "DETERMINACIÓN DE LA GRAVEDAD ESPECIFICA DE SOLIDOS MEDIANTE EL PICOMETRO DE AGUA DE UN SUELO MTC E108",
        "qs": qs,
    }
    return render(request, 'labs/sectors/general/tests_soil/general_specific_gravity.html', context)
