from django.shortcuts import render

from accounts.models import *
from equipments.models import *
from thesis.models import *
from tests_concrete.models import *
from tests_soil.models import *

# Create your views here.

def sector_bach_view(request):
    return render(request, 'labs/sectors/bach/bach.html')


def bach_info_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        qs_users = User.objects.filter(user=request.user)
        context = {
            "title": "Informacion",
            "qs_users": qs_users,
        }
        return render(request, 'labs/sectors/bach/bach_info.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        qs_users = User.objects.filter(is_bach=True)
        qs_thesis = Thesis.objects.all()

        context = {
            "title": "Informacion",
            "qs_users": qs_users,
            "qs_thesis": qs_thesis,
        }
        return render(request, 'labs/sectors/bach/bach_info.html', context)


def bach_equips_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        qs_equips = Equip.objects.all()
        context = {
            "title": "Equipos",
            "qs_equips": qs_equips,
        }
        return render(request, 'labs/sectors/bach/bach_equips.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        qs_equips = Equip.objects.all()
        context = {
            "title": "Equipos",
            "qs_equips": qs_equips,
        }
        return render(request, 'labs/sectors/bach/bach_equips.html', context)


def bach_personal_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        qs_teachers = User.objects.filter(is_teacher=True)

        context = {
            "title": "Personal",
            "qs_teachers": qs_teachers,
        }
        return render(request, 'labs/sectors/bach/bach_personal.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        qs_teachers = User.objects.filter(is_teacher=True)

        context = {
            "title": "Personal",
            "qs_teachers": qs_teachers,
        }
        return render(request, 'labs/sectors/bach/bach_personal.html', context)


def bach_laboratories_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        context = {
            "title": "Laboratorios",
        }
        return render(request, 'labs/sectors/bach/bach_laboratories.html', context)

    elif request.user.is_superuser or request.user.is_admin:

        qs_DiamondPiceBreak = DiamondPiceBreak.objects.filter(user__is_bach=True)
        qs_GroutDiceBreak   = GroutDiceBreak.objects.filter(user__is_bach=True)
        qs_LimeDiceBreak    = LimeDiceBreak.objects.filter(user__is_bach=True)
        qs_LimePiceBreak    = LimePiceBreak.objects.filter(user__is_bach=True)
        qs_PaverBreak       = PaverBreak.objects.filter(user__is_bach=True)
        qs_PiceBreak        = PiceBreak.objects.filter(user__is_bach=True)

        qs_Equivalent           = Equivalent.objects.filter(user__is_bach=True)
        qs_FineMaterial         = FineMaterial.objects.filter(user__is_bach=True)
        qs_GranulometricGlobal  = GranulometricGlobal.objects.filter(user__is_bach=True)
        qs_Limit                = Limit.objects.filter(user__is_bach=True)
        qs_MoistureContent      = MoistureContent.objects.filter(user__is_bach=True)
        qs_ProctorM             = ProctorM.objects.filter(user__is_bach=True)
        qs_SandCone             = SandCone.objects.filter(user__is_bach=True)
        qs_SpecificGravity      = SpecificGravity.objects.filter(user__is_bach=True)

        context = {
            "title": "Laboratorios",
            "qs_DiamondPiceBreak": qs_DiamondPiceBreak,
            "qs_GroutDiceBreak": qs_GroutDiceBreak,
            "qs_LimeDiceBreak": qs_LimeDiceBreak,
            "qs_LimePiceBreak": qs_LimePiceBreak,
            "qs_PaverBreak": qs_PaverBreak,
            "qs_PiceBreak": qs_PiceBreak,
            "qs_Equivalent": qs_Equivalent,
            "qs_FineMaterial": qs_FineMaterial,
            "qs_GranulometricGlobal": qs_GranulometricGlobal,
            "qs_Limit": qs_Limit,
            "qs_MoistureContent": qs_MoistureContent,
            "qs_ProctorM": qs_ProctorM,
            "qs_SandCone": qs_SandCone,
            "qs_SpecificGravity": qs_SpecificGravity,
        }
        return render(request, 'labs/sectors/bach/bach_laboratories.html', context)