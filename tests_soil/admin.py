from django.contrib import admin

from .models import *

# Register your models here.
class LiquidAdmin(admin.TabularInline):
    model = Liquid
    fields = (
        "bowl", "hit", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    readonly_fields = (
        "bowl", "hit", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    extra = 0
    can_delete = False


class PlasticAdmin(admin.TabularInline):
    model = Platic
    fields = (
        "bowl", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    readonly_fields = (
        "bowl", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    extra = 0
    can_delete = False


class LimitAdmin(admin.ModelAdmin):
    list_display = [
        "user", "pit", "layer", "code", "extraction_data", "done_data", "duration", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [LiquidAdmin, PlasticAdmin,]

admin.site.register(Limit, LimitAdmin)


class FineMaterialAdmin(admin.ModelAdmin):
    list_display = [
        "user", "pit", "layer", "code", "sampling_date", "done_date", "duration", 
        "bowl", "before_weight", "bowl_weight", "after_weight", "pass_weight", "fine", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(FineMaterial, FineMaterialAdmin)


class EquivAdmin(admin.TabularInline):
    model = Equiv
    fields = (
        "max_size", "start_sat_time", "out_sat_time", "start_dec_time", "out_dec_time", 
        "max_high_fine", "max_high_sand", "equiv_sand", "equivalent",
    )
    readonly_fields = (
        "max_size", "start_sat_time", "out_sat_time", "start_dec_time", "out_dec_time", 
        "max_high_fine", "max_high_sand", "equiv_sand", "equivalent",
    )
    extra = 0
    can_delete = False


class EquivalentAdmin(admin.ModelAdmin):
    list_display = [
        "user", "pit", "layer", "code", "sampling_date", "done_date", "dilate", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [EquivAdmin,]

admin.site.register(Equivalent, EquivalentAdmin)


class DensityAdmin(admin.TabularInline):
    model = DensityWetDry
    fields = (
        "layers", "hits", "material_weight_P", "bowl_weight_P", "compacted_weight_P", "bowl_volume_P", "wet_density", 
        "bowl", "bowl_weight", "wet_weight", "dry_weight", "water_weight", "material_weight", "moisture", "dry_density",
    )
    readonly_fields = (
        "layers", "hits", "material_weight_P", "bowl_weight_P", "compacted_weight_P", "bowl_volume_P", "wet_density", 
        "bowl", "bowl_weight", "wet_weight", "dry_weight", "water_weight", "material_weight", "moisture", "dry_density",
    )
    extra = 0
    can_delete = False


class SaturationAdmin(admin.TabularInline):
    model = Saturation
    fields = (
        "frac_extrad_weight", "frac_gruesa_weight", "frac_fina_weight", "p_sp_frac_extrad", "p_sp_frac_gruesa", "g_sp_frac_fina", 
        "g_frac_fina_gruesa", "g_sp_global",
    )
    readonly_fields = (
        "frac_extrad_weight", "frac_gruesa_weight", "frac_fina_weight", "p_sp_frac_extrad", "p_sp_frac_gruesa", "g_sp_frac_fina", 
        "g_frac_fina_gruesa", "g_sp_global",
    )
    extra = 0
    can_delete = False


class CorrectionAdmin(admin.TabularInline):
    model = Correction
    fields = (
        "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    readonly_fields = (
        "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    extra = 0
    can_delete = False


class ProctorMAdmin(admin.ModelAdmin):
    list_display = [
        "user", "material", "quarry", "code", "sampling_date", "done_date", "dilate", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [DensityAdmin, SaturationAdmin, CorrectionAdmin]

admin.site.register(ProctorM, ProctorMAdmin)


class MoistureMaterialAdmin(admin.TabularInline):
    model = MoistureMaterial
    fields = (
        "material", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    readonly_fields = (
        "material", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "material_weight", "moisture",
    )
    extra = 0
    can_delete = False


class MoistureContentAdmin(admin.ModelAdmin):
    list_display = [
        "user", "material", "quarry", "code", "sampling_date", "done_date", "dilate", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [MoistureMaterialAdmin,]

admin.site.register(MoistureContent, MoistureContentAdmin)


class FractionPassAddmin(admin.TabularInline):
    model = FractionPass
    fields = (
        "material_pass", "temperature", "water_density", "pycnometer_volume",  
        "pycnometer_mass", "mass_pycnometer_water", "sample_mass", "mass_pyc_w_sample",
        "mass_bowl", "mass_bowl_sample", "mass_dry_sample", "gravity_specific",
        "coefficient_water", "gravity_specific_real",
    )
    readonly_fields = (
        "material_pass", "temperature", "water_density", "pycnometer_volume",  
        "pycnometer_mass", "mass_pycnometer_water", "sample_mass", "mass_pyc_w_sample",
        "mass_bowl", "mass_bowl_sample", "mass_dry_sample", "gravity_specific",
        "coefficient_water", "gravity_specific_real",
    )
    extra = 0
    can_delete = False


class FractionRetainedAddmin(admin.TabularInline):
    model = FractionRetained
    fields = (
        "material_retained", "temperature_23", "saturated_sample", "w_basket_water",  
        "w_basket_water_sample", "w_bowl", "w_bowl_sample", "w_sample_dry",
        "w_sample_sat_water", "specific_grav_mass", "specific_grav_mass_sss", "apparent_spe_gravity",
        "coefficient_water", "specific_mass_weight", "specific_mass_weight_sss", "specific_mass_weight_app", "absorption",
    )
    readonly_fields = (
        "material_retained", "temperature_23", "saturated_sample", "w_basket_water",  
        "w_basket_water_sample", "w_bowl", "w_bowl_sample", "w_sample_dry",
        "w_sample_sat_water", "specific_grav_mass", "specific_grav_mass_sss", "apparent_spe_gravity",
        "coefficient_water", "specific_mass_weight", "specific_mass_weight_sss", "specific_mass_weight_app", "absorption",
    )
    extra = 0
    can_delete = False


class SpecificGravityAdmin(admin.ModelAdmin):
    list_display = [
        "user", "material", "quarry", "code", "sampling_date", "done_date", "dilate", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [FractionPassAddmin, FractionRetainedAddmin]

admin.site.register(SpecificGravity, SpecificGravityAdmin)


class GranulometricGlobalAdmin(admin.ModelAdmin):
    list_display = [
        "user", "quarry", "layer", "code", "sampling_date", "done_date", "dilate", 
        "tamiz_1_1o2", "tamiz_1", "tamiz_3o4", "tamiz_1o2", "tamiz_3o8", "tamiz_4", "tamiz_10", "tamiz_20", "tamiz_40", "tamiz_60", "tamiz_100", "tamiz_200", "tamiz_fondo",
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(GranulometricGlobal, GranulometricGlobalAdmin)


class HumidDensityAdmin(admin.TabularInline):
    model = HumidDensity
    fields = (
        'bowl_weight_sand', 'bowl_weight_remaining_sand', 'weight_sand', 'weight_sand_cone_plate', 'weight_sand_excavation',
        'sand_density', 'volume_material_extracted', 'sample_weight_container', 'container_weight', 'wet_sample_weight', 'density_wet_sample',
    )
    readonly_fields = (
        'bowl_weight_sand', 'bowl_weight_remaining_sand', 'weight_sand', 'weight_sand_cone_plate', 'weight_sand_excavation',
        'sand_density', 'volume_material_extracted', 'sample_weight_container', 'container_weight', 'wet_sample_weight', 'density_wet_sample',
    )
    extra = 0
    can_delete = False


class ContentMoistureAdmin(admin.TabularInline):
    model = ContentMoisture
    fields = (
        'sample_fraction_pass', 'bowl_weight', 'wet_sample_weight_bowl', 'dry_sample_weight_bowl',
        'weight_water','dry_sample_weight', 'sample_moisture',
    )
    readonly_fields = (
        'sample_fraction_pass', 'bowl_weight', 'wet_sample_weight_bowl', 'dry_sample_weight_bowl',
        'weight_water','dry_sample_weight', 'sample_moisture',
    )
    extra = 0
    can_delete = False


class ContentMoistureCarbureAdmin(admin.TabularInline):
    model = ContentMoistureCarbure
    fields = (
        'wet_weight_percentage', 'dry_weight_percentage',
    )
    readonly_fields = (
        'wet_weight_percentage', 'dry_weight_percentage',
    )
    extra = 0
    can_delete = False


class CorrectionSandConeAdmin(admin.TabularInline):
    model = CorrectionSandCone
    fields = (
        'wet_fraction_weight', 'p_e_ap_frac_extrad', 'per_abs_tails_extrad', 'weight_fraction_extrad',
    )
    readonly_fields = (
        'wet_fraction_weight', 'p_e_ap_frac_extrad', 'per_abs_tails_extrad', 'weight_fraction_extrad',
    )
    extra = 0
    can_delete = False


class SandConeAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'sampling_name', 'progressive_sector', 'section_level', 'element_side', 'layer',
        'weight_dry_max', 'opt_moisture', 'moisture', 'code', 'sampling_date', 'done_date', 'dilate',
        'course', 'reference_person', 'construction', 'created', 'updated',
    ]
    inlines = [HumidDensityAdmin, ContentMoistureAdmin, ContentMoistureCarbureAdmin, CorrectionSandConeAdmin]

admin.site.register(SandCone, SandConeAdmin)
