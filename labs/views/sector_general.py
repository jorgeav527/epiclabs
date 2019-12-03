from django.shortcuts import render

from accounts.models import *
from equipments.models import *

# Create your views here.

def general_view(request):
    return render(request, 'labs/sectors/general/general.html')


def general_personal_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_teachers = User.objects.filter(is_teacher=True)
        qs_admins = User.objects.filter(is_admin=True)

    context = {
        "title": "Personal",
        "qs_admins": qs_admins,
        "qs_teachers": qs_teachers,
    }

    return render(request, 'labs/sectors/general/general_personal.html', context)


def general_equips_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_equips = Equip.objects.all()

    context = {
        "title": "Personal",
        "qs_equips": qs_equips,
    }
    
    return render(request, 'labs/sectors/general/general_equips.html', context)