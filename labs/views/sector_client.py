from django.shortcuts import render

from accounts.models import *
from equipments.models import *
from reference_person.models import *
from construction.models import *
from tests_concrete.models import *
from tests_soil.models import *

# Create your views here.

def sector_client_view(request):
    return render(request, 'labs/sectors/client/client.html')

def client_info_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        qs_users = User.objects.filter(user=request.user)
        context = {
            "title": "Informacion",
            "qs_users": qs_users,
        }
        return render(request, 'labs/sectors/client/client_info.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        qs_users = User.objects.filter(is_client=True)
        qs_ref_persons = ReferencePerson.objects.all()
        qs_construcs = Construction.objects.all()

        context = {
            "title": "Informacion",
            "qs_users": qs_users,
            "qs_ref_persons": qs_ref_persons,
            "qs_construcs": qs_construcs,
        }
        return render(request, 'labs/sectors/client/client_info.html', context)


def client_equips_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        qs_equips = Equip.objects.all()
        context = {
            "title": "Equipos",
            "qs_equips": qs_equips,
        }
        return render(request, 'labs/sectors/client/client_equips.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        qs_equips = Equip.objects.all()
        context = {
            "title": "Equipos",
            "qs_equips": qs_equips,
        }
        return render(request, 'labs/sectors/client/client_equips.html', context)


def client_personal_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        qs_admins = User.objects.filter(is_admin=True)

        context = {
            "title": "Personal",
            "qs_admins": qs_admins,
        }
        return render(request, 'labs/sectors/client/client_personal.html', context)

    elif request.user.is_superuser or request.user.is_admin:
        qs_admins = User.objects.filter(is_admin=True)

        context = {
            "title": "Personal",
            "qs_admins": qs_admins,
        }
        return render(request, 'labs/sectors/client/client_personal.html', context)


def client_laboratories_view(request):

    if request.user.is_bach or request.user.is_student or request.user.is_client:
        context = {
            "title": "Laboratorios",
        }
        return render(request, 'labs/sectors/client/client_laboratories.html', context)

    elif request.user.is_superuser or request.user.is_admin:

        qs_DiamondPiceBreak = DiamondPiceBreak.objects.filter(user__is_client=True)
        qs_GroutDiceBreak   = GroutDiceBreak.objects.filter(user__is_client=True)
        qs_LimeDiceBreak    = LimeDiceBreak.objects.filter(user__is_client=True)
        qs_LimePiceBreak    = LimePiceBreak.objects.filter(user__is_client=True)
        qs_PaverBreak       = PaverBreak.objects.filter(user__is_client=True)
        qs_PiceBreak        = PiceBreak.objects.filter(user__is_client=True)

        qs_Equivalent           = Equivalent.objects.filter(user__is_client=True)
        qs_FineMaterial         = FineMaterial.objects.filter(user__is_client=True)
        qs_GranulometricGlobal  = GranulometricGlobal.objects.filter(user__is_client=True)
        qs_Limit                = Limit.objects.filter(user__is_client=True)
        qs_MoistureContent      = MoistureContent.objects.filter(user__is_client=True)
        qs_ProctorM             = ProctorM.objects.filter(user__is_client=True)
        qs_SandCone             = SandCone.objects.filter(user__is_client=True)
        qs_SpecificGravity      = SpecificGravity.objects.filter(user__is_client=True)

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
        return render(request, 'labs/sectors/client/client_laboratories.html', context)