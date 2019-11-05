from django.shortcuts import render

def tests_material_info_view(request):
    context = {
        "title": "Materiales de Construcción Información",
    }
    return render(request, 'tests_material/info_tests_material.html', context)


def tests_material_equips_view(request):
    context = {
        "title": "Materiales de Construcción Equipos",
    }
    return render(request, 'tests_material/equips_tests_material.html', context)


def tests_material_guides_view(request):
    context = {
        "title": "Materiales de Construcción Guias de los Ensayos",
    }
    return render(request, 'tests_material/guides_tests_material.html', context)


def tests_material_teachers_view(request):
    context = {
        "title": "Materiales de Construcción Plana Docente",
    }
    return render(request, 'tests_material/teachers_tests_material.html', context)