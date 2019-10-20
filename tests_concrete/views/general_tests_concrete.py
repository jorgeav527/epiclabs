from django.shortcuts import render

def tests_concrete_info_view(request):
    context = {
        "title": "Tecnología del Concreto Información",
    }
    return render(request, 'tests_concrete/info_tests_concrete.html', context)


def tests_concrete_equips_view(request):
    context = {
        "title": "Tecnología del Concreto Equipos",
    }
    return render(request, 'tests_concrete/equips_tests_concrete.html', context)


def tests_concrete_guides_view(request):
    context = {
        "title": "Tecnología del Concreto Guias de los Ensayos",
    }
    return render(request, 'tests_concrete/guides_tests_concrete.html', context)


def tests_concrete_teachers_view(request):
    context = {
        "title": "Tecnología del Concreto Plana Docente",
    }
    return render(request, 'tests_concrete/teachers_tests_concrete.html', context)