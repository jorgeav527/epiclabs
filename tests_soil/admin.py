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


class ProctorMAdmin(admin.ModelAdmin):
    list_display = [
        "user", "material", "quarry", "code", "sampling_date", "done_date", "dilate", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [DensityAdmin, SaturationAdmin, CorrectionAdmin]

admin.site.register(ProctorM, ProctorMAdmin)

