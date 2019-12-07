from django.shortcuts import render
import numpy as np

from accounts.models import *
from equipments.models import *
from reference_person.models import *
from construction.models import *
from tests_concrete.models import *
from tests_soil.models import *

# Create your views here.

def sector_client_view(request):
    return render(request, 'labs/sectors/client/client.html')


def client_info_clients_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_users = User.objects.filter(is_client=True)

        context = {
            "title": "Informacion",
            "qs_users": qs_users,
        }
        return render(request, 'labs/sectors/client/client_info_clients.html', context)


def client_info_ref_per_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_ref_persons = ReferencePerson.objects.all()

        context = {
            "title": "Informacion",
            "qs_ref_persons": qs_ref_persons,
        }
        return render(request, 'labs/sectors/client/client_info_ref_per.html', context)


def client_info_construction_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_constructions = Construction.objects.all()

        context = {
            "title": "Informacion",
            "qs_constructions": qs_constructions,
        }
        return render(request, 'labs/sectors/client/client_info_construction.html', context)


def client_equips_concrete_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_equips = Equip.objects.all()
        qs_equips_names = qs_equips.values_list("name", flat=True)
        qs_DiamondPiceBreak_equips = []
        qs_GroutDiceBreak_equips = []
        qs_LimeDiceBreak_equips = []
        qs_LimePiceBreak_equips = []
        qs_PaverBreak_equips = []
        qs_PiceBreak_equips = []
        
        for name in qs_equips_names:

            qs_DiamondPiceBreak = Equip.objects.get(name=name).diamondpicebreak_set.filter(user__is_client=True).count()
            qs_GroutDiceBreak = Equip.objects.get(name=name).groutdicebreak_set.filter(user__is_client=True).count()
            qs_LimeDiceBreak = Equip.objects.get(name=name).limedicebreak_set.filter(user__is_client=True).count()
            qs_LimePiceBreak = Equip.objects.get(name=name).limepicebreak_set.filter(user__is_client=True).count()
            qs_PaverBreak = Equip.objects.get(name=name).paverbreak_set.filter(user__is_client=True).count()
            qs_PiceBreak = Equip.objects.get(name=name).picebreak_set.filter(user__is_client=True).count()

            qs_DiamondPiceBreak_equips.append(qs_DiamondPiceBreak)
            qs_GroutDiceBreak_equips.append(qs_GroutDiceBreak)
            qs_LimeDiceBreak_equips.append(qs_LimeDiceBreak)
            qs_LimePiceBreak_equips.append(qs_LimePiceBreak)
            qs_PaverBreak_equips.append(qs_PaverBreak)
            qs_PiceBreak_equips.append(qs_PiceBreak)

        context = {
            "title": "Equipos",
            "qs_equips_names": qs_equips_names,
            "qs_DiamondPiceBreak_equips": qs_DiamondPiceBreak_equips,
            "qs_GroutDiceBreak_equips": qs_GroutDiceBreak_equips,
            "qs_LimeDiceBreak_equips": qs_LimeDiceBreak_equips,
            "qs_LimePiceBreak_equips": qs_LimePiceBreak_equips,
            "qs_PaverBreak_equips": qs_PaverBreak_equips,
            "qs_PiceBreak_equips": qs_PiceBreak_equips,
        }
        return render(request, 'labs/sectors/client/client_equips_concrete.html', context)


def client_equips_soil_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_equips = Equip.objects.all()
        qs_equips_names = qs_equips.values_list("name", flat=True)
        qs_Equivalent_equips = []
        qs_Equiv_equips = []
        qs_FineMaterial_equips = []
        qs_GranulometricGlobal_equips = []
        qs_Limit_equips = []
        qs_Liquid_equips = []
        qs_Platic_equips = []
        qs_MoistureContent_equips = []
        qs_MoistureMaterial_equips = []
        qs_ProctorM_equips = []
        qs_DensityWetDry_equips = []
        qs_Saturation_equips = []
        qs_Correction_equips = []
        qs_SandCone_equips = []
        qs_HumidDensity_equips = []
        qs_ContentMoisture_equips = []
        qs_ContentMoistureCarbure_equips = []
        qs_CorrectionSandCone_equips = []
        qs_SpecificGravity_equips = []
        qs_FractionPass_equips = []
        qs_FractionRetained_equips = []
        
        for name in qs_equips_names:

            qs_Equivalent = Equip.objects.get(name=name).equivalent_set.filter(user__is_client=True).count()
            qs_Equiv = Equip.objects.get(name=name).equiv_set.filter(equivalent__user__is_client=True).count()
            qs_FineMaterial = Equip.objects.get(name=name).finematerial_set.filter(user__is_client=True).count()
            qs_GranulometricGlobal = Equip.objects.get(name=name).granulometricglobal_set.filter(user__is_client=True).count()
            qs_Limit = Equip.objects.get(name=name).limit_set.filter(user__is_client=True).count()
            qs_Liquid = Equip.objects.get(name=name).liquid_set.filter(limit__user__is_client=True).count()
            qs_Platic = Equip.objects.get(name=name).platic_set.filter(limit__user__is_client=True).count()
            qs_MoistureContent = Equip.objects.get(name=name).moisturecontent_set.filter(user__is_client=True).count()
            qs_MoistureMaterial = Equip.objects.get(name=name).moisturematerial_set.filter(moisture_content__user__is_client=True).count()
            qs_ProctorM = Equip.objects.get(name=name).proctorm_set.filter(user__is_client=True).count()
            qs_DensityWetDry = Equip.objects.get(name=name).densitywetdry_set.filter(proctor_m__user__is_client=True).count()
            qs_Saturation = Equip.objects.get(name=name).saturation_set.filter(proctor_m__user__is_client=True).count()
            qs_Correction = Equip.objects.get(name=name).correction_set.filter(proctor_m__user__is_client=True).count()
            qs_SandCone = Equip.objects.get(name=name).sandcone_set.filter(user__is_client=True).count()
            qs_HumidDensity = Equip.objects.get(name=name).humiddensity_set.filter(sand_cone__user__is_client=True).count()
            qs_ContentMoisture = Equip.objects.get(name=name).contentmoisture_set.filter(sand_cone__user__is_client=True).count()
            qs_ContentMoistureCarbure = Equip.objects.get(name=name).contentmoisturecarbure_set.filter(sand_cone__user__is_client=True).count()
            qs_CorrectionSandCone = Equip.objects.get(name=name).correctionsandcone_set.filter(sand_cone__user__is_client=True).count()
            qs_SpecificGravity = Equip.objects.get(name=name).specificgravity_set.filter(user__is_client=True).count()
            qs_FractionPass = Equip.objects.get(name=name).fractionpass_set.filter(specific_gravity__user__is_client=True).count()
            qs_FractionRetained = Equip.objects.get(name=name).fractionretained_set.filter(specific_gravity__user__is_client=True).count()

            qs_Equivalent_equips.append(qs_Equivalent)
            qs_Equiv_equips.append(qs_Equiv)
            qs_FineMaterial_equips.append(qs_FineMaterial)
            qs_GranulometricGlobal_equips.append(qs_GranulometricGlobal)
            qs_Limit_equips.append(qs_Limit)
            qs_Liquid_equips.append(qs_Liquid)
            qs_Platic_equips.append(qs_Platic)
            qs_MoistureContent_equips.append(qs_MoistureContent)
            qs_MoistureMaterial_equips.append(qs_MoistureMaterial)
            qs_ProctorM_equips.append(qs_ProctorM)
            qs_DensityWetDry_equips.append(qs_DensityWetDry)
            qs_Saturation_equips.append(qs_Saturation)
            qs_Correction_equips.append(qs_Correction)
            qs_SandCone_equips.append(qs_SandCone)
            qs_HumidDensity_equips.append(qs_HumidDensity)
            qs_ContentMoisture_equips.append(qs_ContentMoisture)
            qs_ContentMoistureCarbure_equips.append(qs_ContentMoistureCarbure)
            qs_CorrectionSandCone_equips.append(qs_CorrectionSandCone)
            qs_SpecificGravity_equips.append(qs_SpecificGravity)
            qs_FractionPass_equips.append(qs_FractionPass)
            qs_FractionRetained_equips.append(qs_FractionRetained)

        qs_Equivalent_Equiv = np.add(qs_Equivalent_equips, qs_Equiv_equips)
        qs_Limit_Liquid = np.add(qs_Limit_equips, qs_Liquid_equips)
        qs_Liquid_Platic = np.add(qs_Limit_Liquid, qs_Platic_equips)
        qs_MoistureContent_MoistureMaterial = np.add(qs_MoistureContent_equips, qs_MoistureMaterial_equips)
        qs_ProctorM_DensityWetDry = np.add(qs_ProctorM_equips, qs_DensityWetDry_equips)
        qs_DensityWetDry_Saturation = np.add(qs_ProctorM_DensityWetDry, qs_Saturation_equips)
        qs_Saturation_Correction = np.add(qs_DensityWetDry_Saturation, qs_Correction_equips)
        qs_SandCone_HumidDensity = np.add(qs_SandCone_equips, qs_HumidDensity_equips)
        qs_HumidDensity_ContentMoisture = np.add(qs_SandCone_HumidDensity, qs_ContentMoisture_equips)
        qs_ContentMoisture_ContentMoistureCarbure = np.add(qs_HumidDensity_ContentMoisture, qs_ContentMoistureCarbure_equips)
        qs_ContentMoistureCarbure_CorrectionSandCone = np.add(qs_ContentMoisture_ContentMoistureCarbure, qs_CorrectionSandCone_equips)
        qs_SpecificGravity_FractionPass = np.add(qs_SpecificGravity_equips, qs_FractionPass_equips)
        qs_FractionPass_FractionRetained = np.add(qs_SpecificGravity_FractionPass, qs_FractionRetained_equips)
        
        context = {
            "title": "Equipos",
            "qs_equips_names": qs_equips_names,
            "qs_Equivalent_Equiv": qs_Equivalent_Equiv,
            "qs_FineMaterial_equips": qs_FineMaterial_equips,
            "qs_GranulometricGlobal_equips": qs_GranulometricGlobal_equips,
            "qs_Liquid_Platic": qs_Liquid_Platic,
            "qs_MoistureContent_MoistureMaterial": qs_MoistureContent_MoistureMaterial,
            "qs_Saturation_Correction": qs_Saturation_Correction,
            "qs_ContentMoistureCarbure_CorrectionSandCone": qs_ContentMoistureCarbure_CorrectionSandCone,
            "qs_FractionPass_FractionRetained": qs_FractionPass_FractionRetained,
        }

        return render(request, 'labs/sectors/client/client_equips_soil.html', context)


def client_tests_concrete_view(request):

    if request.user.is_superuser or request.user.is_admin:

        qs_DiamondPiceBreak = DiamondPiceBreak.objects.filter(user__is_client=True)
        qs_GroutDiceBreak   = GroutDiceBreak.objects.filter(user__is_client=True)
        qs_LimeDiceBreak    = LimeDiceBreak.objects.filter(user__is_client=True)
        qs_LimePiceBreak    = LimePiceBreak.objects.filter(user__is_client=True)
        qs_PaverBreak       = PaverBreak.objects.filter(user__is_client=True)
        qs_PiceBreak        = PiceBreak.objects.filter(user__is_client=True)

        context = {
            "title": "Laboratorios",
            "qs_DiamondPiceBreak": qs_DiamondPiceBreak,
            "qs_GroutDiceBreak": qs_GroutDiceBreak,
            "qs_LimeDiceBreak": qs_LimeDiceBreak,
            "qs_LimePiceBreak": qs_LimePiceBreak,
            "qs_PaverBreak": qs_PaverBreak,
            "qs_PiceBreak": qs_PiceBreak,
        }
        return render(request, 'labs/sectors/client/client_tests_concrete.html', context)


def client_tests_soil_view(request):

    if request.user.is_superuser or request.user.is_admin:

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
            "qs_Equivalent": qs_Equivalent,
            "qs_FineMaterial": qs_FineMaterial,
            "qs_GranulometricGlobal": qs_GranulometricGlobal,
            "qs_Limit": qs_Limit,
            "qs_MoistureContent": qs_MoistureContent,
            "qs_ProctorM": qs_ProctorM,
            "qs_SandCone": qs_SandCone,
            "qs_SpecificGravity": qs_SpecificGravity,
        }
        return render(request, 'labs/sectors/client/client_tests_soil.html', context)