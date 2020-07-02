from django.shortcuts import render
import numpy as np

from bokeh.core.properties import value
from bokeh.plotting import figure
from bokeh.embed import components

from accounts.models import *
from equipments.models import *
from reference_person.models import *
from construction.models import *
from tests_concrete.models import *
from tests_material.models import *
from tests_soil.models import *

# STUDENT SECTOR REUSE FUNCTIONS
#==============================

def graph_student_sector(equips, tests, colors, data):
    TOOLS="hover,pan,wheel_zoom,reset,save"
    plot = figure(x_range=equips, plot_height=500, plot_width=800, title="Numero de Usos vs Equipos", 
        tools=TOOLS, y_axis_label= 'Numero de Usos', tooltips="@equips: @$name",
        sizing_mode="fixed",)

    plot.vbar_stack(tests, x='equips', width=0.5, color=colors, source=data, legend=[value(x) for x in tests])

    plot.y_range.start = 0
    plot.legend.location = "top_right"
    plot.xgrid.grid_line_color = None
    plot.xaxis.major_label_orientation = 1
    script, div = components(plot)

    return script, div

# STUDENT VIEWS USERS
#===================

def sector_student_view(request):
    return render(request, 'labs/sectors/student/student.html')


def sector_student_info_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_users = User.objects.filter(is_group=True)

        context = {
            "title": "Infordmación de Estudiantes",
            "qs_users": qs_users,
        }
        return render(request, 'labs/sectors/student/info/student_info_students.html', context)


def student_equips_concrete_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_equips = Equip.objects.all()
        qs_equips_names = qs_equips.values_list("name", flat=True)
        qs_DiamondPiceBreak_equips = []
        qs_DiamondPice_equips = []
        qs_PiceBreak_equips = []
        qs_Pice_equips = []
        qs_PrismBreak_equips = []
        qs_Prism_equips = []
        
        for name in qs_equips_names:

            qs_DiamondPiceBreak = Equip.objects.get(name=name).diamondpicebreak_set.filter(user__is_group=True).count()
            qs_DiamondPice = Equip.objects.get(name=name).diamondpice_set.filter(diamond_pice_break__user__is_group=True).count()
            qs_PiceBreak = Equip.objects.get(name=name).picebreak_set.filter(user__is_group=True).count()
            qs_Pice = Equip.objects.get(name=name).pice_set.filter(pice_break__user__is_group=True).count()
            qs_PrismBreak = Equip.objects.get(name=name).prismbreak_set.filter(user__is_group=True).count()
            qs_Prism = Equip.objects.get(name=name).prism_set.filter(prism_break__user__is_group=True).count()

            qs_DiamondPiceBreak_equips.append(qs_DiamondPiceBreak)
            qs_DiamondPice_equips.append(qs_DiamondPice)
            qs_PiceBreak_equips.append(qs_PiceBreak)
            qs_Pice_equips.append(qs_Pice)
            qs_PrismBreak_equips.append(qs_PrismBreak)
            qs_Prism_equips.append(qs_Prism)

        qs_sum_equips_DiamondPiceBreak = list(map(sum, zip(
            qs_DiamondPiceBreak_equips, 
            qs_DiamondPice_equips, 
        )))

        qs_sum_equips_PiceBreak = list(map(sum, zip(
            qs_PiceBreak_equips, 
            qs_Pice_equips, 
        )))

        qs_sum_equips_PrismBreak = list(map(sum, zip(
            qs_PrismBreak_equips, 
            qs_Prism_equips, 
        )))

        equips = list(qs_equips_names)
        tests = ["Compresión de Testigos", "Compresión de Prismas", "Compresión de Testigos Diamantinos"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]

        data = {
            'equips' : equips,
            'Compresión de Testigos': qs_sum_equips_DiamondPiceBreak,
            'Compresión de Prismas': qs_sum_equips_PiceBreak,
            'Compresión de Testigos Diamantinos': qs_sum_equips_PrismBreak,
        }

        graph = graph_student_sector(equips, tests, colors, data)
        script = graph[0]
        div = graph[1]

        context = {
            "script": script,
            "div": div,
            "title": "Equipos Usados en el Laboratorio de Tecnología del Concreto",
            "qs_equips_names": qs_equips_names,
            "qs_sum_equips_DiamondPiceBreak": qs_sum_equips_DiamondPiceBreak,
            "qs_sum_equips_PiceBreak": qs_sum_equips_PiceBreak,
            "qs_sum_equips_PrismBreak": qs_sum_equips_PrismBreak,
        }
        return render(request, 'labs/sectors/student/equips/student_equips_concrete.html', context)


def student_equips_material_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_equips = Equip.objects.all()
        qs_equips_names = qs_equips.values_list("name", flat=True)
        qs_BrickType_equips = []
        qs_VariationDimensions_equips = []
        qs_Warping_equips = []
        qs_DensityVoids_equips = []
        qs_Suction_equips = []
        qs_AbsSatuCoeff_equips = []
        qs_CompretionBrick_equips = []
        qs_WoodCompression_equips = []
        qs_ParallelPerpendicular_equips = []
        qs_MasonryCompression_equips = []
        qs_Masonry_equips = []
        
        for name in qs_equips_names:

            qs_BrickType = Equip.objects.get(name=name).bricktype_set.filter(user__is_group=True).count()
            qs_VariationDimensions =Equip.objects.get(name=name).variationdimensions_set.filter(brick_type__user__is_group=True).count()
            qs_Warping =Equip.objects.get(name=name).warping_set.filter(brick_type__user__is_group=True).count()
            qs_DensityVoids =Equip.objects.get(name=name).densityvoids_set.filter(brick_type__user__is_group=True).count()
            qs_Suction =Equip.objects.get(name=name).suction_set.filter(brick_type__user__is_group=True).count()
            qs_AbsSatuCoeff =Equip.objects.get(name=name).abssatucoeff_set.filter(brick_type__user__is_group=True).count()
            qs_CompretionBrick =Equip.objects.get(name=name).compretionbrick_set.filter(brick_type__user__is_group=True).count()
            qs_WoodCompression = Equip.objects.get(name=name).woodcompression_set.filter(user__is_group=True).count() 
            qs_ParallelPerpendicular =Equip.objects.get(name=name).parallelperpendicular_set.filter(wood_compression__user__is_group=True).count()
            qs_MasonryCompression =Equip.objects.get(name=name).masonrycompression_set.filter(user__is_group=True).count()
            qs_Masonry =Equip.objects.get(name=name).masonry_set.filter(masonry_compression__user__is_group=True).count()

            qs_BrickType_equips.append(qs_BrickType)
            qs_VariationDimensions_equips.append(qs_VariationDimensions)
            qs_Warping_equips.append(qs_Warping)
            qs_DensityVoids_equips.append(qs_DensityVoids)
            qs_Suction_equips.append(qs_Suction)
            qs_AbsSatuCoeff_equips.append(qs_AbsSatuCoeff)
            qs_CompretionBrick_equips.append(qs_CompretionBrick)
            qs_WoodCompression_equips.append(qs_WoodCompression)
            qs_ParallelPerpendicular_equips.append(qs_ParallelPerpendicular)
            qs_MasonryCompression_equips.append(qs_MasonryCompression)
            qs_Masonry_equips.append(qs_Masonry)
        
        qs_sum_equips_BrickType = list(map(sum, zip(
            qs_BrickType_equips, 
            qs_VariationDimensions_equips, 
            qs_Warping_equips, 
            qs_DensityVoids_equips, 
            qs_Suction_equips, 
            qs_AbsSatuCoeff_equips, 
            qs_CompretionBrick_equips
        )))

        qs_sum_equips_WoodCompression = list(map(sum, zip(
            qs_WoodCompression_equips, 
            qs_ParallelPerpendicular_equips, 
        )))

        qs_sum_equips_MasonryCompression = list(map(sum, zip(
            qs_MasonryCompression_equips, 
            qs_Masonry_equips, 
        )))

        equips = list(qs_equips_names)
        tests = ["Clasificación del Ladrillo", "Compresión Simple en Madera", "Compresión de Pilas de Ladrillos"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]

        data = {
            'equips' : equips,
            'Clasificación del Ladrillo': qs_sum_equips_BrickType,
            'Compresión Simple en Madera': qs_sum_equips_WoodCompression,
            'Compresión de Pilas de Ladrillos': qs_sum_equips_MasonryCompression,
        }

        graph = graph_student_sector(equips, tests, colors, data)
        script = graph[0]
        div = graph[1]

        context = {
            "script": script,
            "div": div,
            "title": "Equipos Usados en el Laboratorio de Materiales de Construcción",
            "qs_equips_names": qs_equips_names,
            "qs_sum_equips_BrickType": qs_sum_equips_BrickType,
            "qs_sum_equips_WoodCompression": qs_sum_equips_WoodCompression,
            "qs_sum_equips_MasonryCompression": qs_sum_equips_MasonryCompression,
        }
        return render(request, 'labs/sectors/student/equips/student_equips_material.html', context)


def student_equips_soil_view(request):
    if request.user.is_superuser or request.user.is_admin:
        qs_equips = Equip.objects.all()
        qs_equips_names = qs_equips.values_list("name", flat=True)
        qs_Equivalent_equips = []
        qs_Equiv_equips = []
        qs_FineMaterial_equips = []
        qs_GranulometricGlobal_equips = []
        qs_GlobalMesh_equips = []
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

            qs_Equivalent = Equip.objects.get(name=name).equivalent_set.filter(user__is_group=True).count()
            qs_Equiv = Equip.objects.get(name=name).equiv_set.filter(equivalent__user__is_group=True).count()
            qs_FineMaterial = Equip.objects.get(name=name).finematerial_set.filter(user__is_group=True).count()
            qs_GranulometricGlobal = Equip.objects.get(name=name).granulometricglobal_set.filter(user__is_group=True).count()
            qs_GlobalMesh = Equip.objects.get(name=name).globalmesh_set.filter(granulometric_global__user__is_group=True).count()
            qs_Limit = Equip.objects.get(name=name).limit_set.filter(user__is_group=True).count()
            qs_Liquid = Equip.objects.get(name=name).liquid_set.filter(limit__user__is_group=True).count()
            qs_Platic = Equip.objects.get(name=name).platic_set.filter(limit__user__is_group=True).count()
            qs_MoistureContent = Equip.objects.get(name=name).moisturecontent_set.filter(user__is_group=True).count()
            qs_MoistureMaterial = Equip.objects.get(name=name).moisturematerial_set.filter(moisture_content__user__is_group=True).count()
            qs_ProctorM = Equip.objects.get(name=name).proctorm_set.filter(user__is_group=True).count()
            qs_DensityWetDry = Equip.objects.get(name=name).densitywetdry_set.filter(proctor_m__user__is_group=True).count()
            qs_Saturation = Equip.objects.get(name=name).saturation_set.filter(proctor_m__user__is_group=True).count()
            qs_Correction = Equip.objects.get(name=name).correction_set.filter(proctor_m__user__is_group=True).count()
            qs_SandCone = Equip.objects.get(name=name).sandcone_set.filter(user__is_group=True).count()
            qs_HumidDensity = Equip.objects.get(name=name).humiddensity_set.filter(sand_cone__user__is_group=True).count()
            qs_ContentMoisture = Equip.objects.get(name=name).contentmoisture_set.filter(sand_cone__user__is_group=True).count()
            qs_ContentMoistureCarbure = Equip.objects.get(name=name).contentmoisturecarbure_set.filter(sand_cone__user__is_group=True).count()
            qs_CorrectionSandCone = Equip.objects.get(name=name).correctionsandcone_set.filter(sand_cone__user__is_group=True).count()
            qs_SpecificGravity = Equip.objects.get(name=name).specificgravity_set.filter(user__is_group=True).count()
            qs_FractionPass = Equip.objects.get(name=name).fractionpass_set.filter(specific_gravity__user__is_group=True).count()
            qs_FractionRetained = Equip.objects.get(name=name).fractionretained_set.filter(specific_gravity__user__is_group=True).count()

            qs_Equivalent_equips.append(qs_Equivalent)
            qs_Equiv_equips.append(qs_Equiv)
            qs_FineMaterial_equips.append(qs_FineMaterial)
            qs_GranulometricGlobal_equips.append(qs_GranulometricGlobal)
            qs_GlobalMesh_equips.append(qs_GlobalMesh)
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

        qs_sum_equips_Equivalent = list(map(sum, zip(
            qs_Equivalent_equips, 
            qs_Equiv_equips, 
        )))

        qs_sum_equips_FineMaterial = list(map(sum, zip(
            qs_FineMaterial_equips, 
        )))

        qs_sum_equips_GranulometricGlobal = list(map(sum, zip(
            qs_GranulometricGlobal_equips,
            qs_GlobalMesh_equips,
        )))

        qs_sum_equips_Limit = list(map(sum, zip(
            qs_Limit_equips,
            qs_Liquid_equips,
            qs_Platic_equips,
        )))

        qs_sum_equips_MoistureContent = list(map(sum, zip(
            qs_MoistureContent_equips,
            qs_MoistureMaterial_equips,
        )))

        qs_sum_equips_ProctorM = list(map(sum, zip(
            qs_ProctorM_equips,
            qs_DensityWetDry_equips,
            qs_Saturation_equips,
            qs_Correction_equips,
        )))
        
        qs_sum_equips_SandCone = list(map(sum, zip(
            qs_SandCone_equips,
            qs_HumidDensity_equips,
            qs_ContentMoisture_equips,
            qs_ContentMoistureCarbure_equips,
            qs_CorrectionSandCone_equips,
        )))

        qs_sum_equips_SpecificGravity = list(map(sum, zip(
            qs_SpecificGravity_equips,
            qs_FractionPass_equips,
            qs_FractionRetained_equips,
        )))

        equips = list(qs_equips_names)
        tests = [
            "Valor Equivalente de Arena y Fino",
            "Material más Fino que el Tamiz 75μm (Nro. 200)",
            "Granulometria Global",
            "Límite Líquido y Límite Plástico",
            "Contenido de Humedad de un Suelo",
            "Proctor Modificado",
            "Cono de Arena",
            "Gravedad Especifica mediante el Picómetro de Agua",
        ]
        colors = ["#c9d9d3", "#718dbf", "#e84d60", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen"]

        data = {
            'equips': equips,
            'Valor Equivalente de Arena y Fino': qs_sum_equips_Equivalent,
            'Material más Fino que el Tamiz 75μm (Nro. 200)': qs_sum_equips_FineMaterial,
            'Granulometria Global': qs_sum_equips_GranulometricGlobal,
            'Límite Líquido y Límite Plástico': qs_sum_equips_Limit,
            'Contenido de Humedad de un Suelo': qs_sum_equips_MoistureContent,
            'Proctor Modificado': qs_sum_equips_ProctorM,
            'Cono de Arena': qs_sum_equips_SandCone,
            'Gravedad Especifica mediante el Picómetro de Agua': qs_sum_equips_SpecificGravity,
        }

        graph = graph_student_sector(equips, tests, colors, data)
        script = graph[0]
        div = graph[1]

        context = {
            "script": script,
            "div": div,
            "title": "Equipos Usados en el Laboratorio de Suelos",
            "qs_equips_names": qs_equips_names,
            "qs_sum_equips_Equivalent": qs_sum_equips_Equivalent,
            "qs_sum_equips_FineMaterial": qs_sum_equips_FineMaterial,
            "qs_sum_equips_GranulometricGlobal": qs_sum_equips_GranulometricGlobal,
            "qs_sum_equips_Limit": qs_sum_equips_Limit,
            "qs_sum_equips_MoistureContent": qs_sum_equips_MoistureContent,
            "qs_sum_equips_ProctorM": qs_sum_equips_ProctorM,
            "qs_sum_equips_SandCone": qs_sum_equips_SandCone,
            "qs_sum_equips_SpecificGravity": qs_sum_equips_SpecificGravity,
        }

        return render(request, 'labs/sectors/student/equips/student_equips_soil.html', context)
