from django.shortcuts import render

# Create your views here.

def tests_materials_info_view(request):
    context = {
        "title": "jojojo",
    }
    return render(request, 'tests_material/info.html', context)


def grout_dice_break_view(request):
    context = {
        "title": "la lista de ensayos de dados de grout",
    }
    return render(request, 'tests_material/grout_dice_break_list.html', context)
