from django.shortcuts import render

def tests_soil_info_view(request):
    context = {
        "title": "Mecánica de Suelos Información",
    }
    return render(request, 'tests_soil/info_tests_soil.html', context)


def tests_soil_equips_view(request):
    context = {
        "title": "Mecánica de Suelos Equipos",
    }
    return render(request, 'tests_soil/equips_tests_soil.html', context)


def tests_soil_guides_view(request):
    context = {
        "title": "Mecánica de Suelos Guias de los Ensayos",
    }
    return render(request, 'tests_soil/guides_tests_soil.html', context)


def tests_soil_teachers_view(request):
    context = {
        "title": "Mecánica de Suelos Plana Docente",
    }
    return render(request, 'tests_soil/teachers_tests_soil.html', context)