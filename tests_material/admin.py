from django.contrib import admin

from .models import *

# Register your models here.

class VariationDimensionsAdmin(admin.TabularInline):
    model = VariationDimensions
    fields = (
        "upface_length", "downface_length", "average_length", "upface_width", "downface_width", "average_width", 
        "high_backside", "high_rightside", "high_frontside", "high_lefside", "average_high", 
    )
    readonly_fields = (
        "upface_length", "downface_length", "average_length", "upface_width", "downface_width", "average_width", 
        "high_backside", "high_rightside", "high_frontside", "high_lefside", "average_high", 
    )
    extra = 0
    can_delete = False


class WarpingAdmin(admin.TabularInline):
    model = Warping
    fields = ( 
        "upface_concave", "upface_convex", "downface_concave", "downface_convex",
    )
    readonly_fields = (
        "upface_concave", "upface_convex", "downface_concave", "downface_convex",
    )
    extra = 0
    can_delete = False


class DensityVoidsAdmin(admin.TabularInline):
    model = DensityVoids
    fields = ( 
         "length", "width", "high", "volume_brick", "sc", "su", 
         "volume_void", "volume_real", "void_percentage", "weight", "density",
    )
    readonly_fields = (
         "length", "width", "high", "volume_brick", "sc", "su", 
         "volume_void", "volume_real", "void_percentage", "weight", "density",
    )
    extra = 0
    can_delete = False


class SuctionAdmin(admin.TabularInline):
    model = Suction
    fields = (
        "nomal_weight", "dry_weight", "diff_weight", "length", "width", "face_area", 
        "face_wet_weight", "face_wet_weight_correction",
    )
    readonly_fields = (
        "nomal_weight", "dry_weight", "diff_weight", "length", "width", "face_area", 
        "face_wet_weight", "face_wet_weight_correction",
    )
    extra = 0
    can_delete = False


class AbsSatuCoeffAdmin(admin.TabularInline):
    model = AbsSatuCoeff
    fields = (
        "dry_weight", "wet_weight_cool_24", "wet_weight_hot_5", 
        "abs_brick", "abs_max_brick", "coeff_sat",
    )
    readonly_fields = (
        "dry_weight", "wet_weight_cool_24", "wet_weight_hot_5", 
        "abs_brick", "abs_max_brick", "coeff_sat",
    )
    extra = 0
    can_delete = False


class CompretionBrickAdmin(admin.TabularInline):
    model = CompretionBrick
    fields = (
        "upface_length", "upface_width", "downface_length", "downface_width", "upface_area", "downface_area", 
        "average_area", "load", "fc", "fc_MPa",
    )
    readonly_fields = (
        "upface_length", "upface_width", "downface_length", "downface_width", "upface_area", "downface_area", 
        "average_area", "load", "fc", "fc_MPa",
    )
    extra = 0
    can_delete = False


class BrickTypeAdmin(admin.ModelAdmin):
    list_display = [
        "user", "name_element", "brick_company", "code", "sampling_date", "done_date", "dilate",
        "n_d_length", "n_d_width", "n_d_high",
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [VariationDimensionsAdmin, WarpingAdmin, DensityVoidsAdmin, SuctionAdmin, AbsSatuCoeffAdmin, CompretionBrickAdmin]

admin.site.register(BrickType, BrickTypeAdmin)


class ParallelPerpendicularAdmin(admin.TabularInline):
    model = ParallelPerpendicular
    fields = ( 
        "type_compression", "length_1", "width_1", "area_1", "length_2", "width_2", "area_2", 
        "average_area", "load", "fc", "fc_MPa",
    )
    readonly_fields = (
        "type_compression", "length_1", "width_1", "area_1", "length_2", "width_2", "area_2", 
        "average_area", "load", "fc", "fc_MPa",
    )
    extra = 0
    can_delete = False


class WoodCompressionAdmin(admin.ModelAdmin):
    list_display = [ 
        "user", "name", "name_element", "wood_name", "code", "sampling_date", "done_date", "dilate", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [ParallelPerpendicularAdmin]

admin.site.register(WoodCompression, WoodCompressionAdmin)


class MasonryAdmin(admin.TabularInline):
    model = Masonry
    fields = ( 
        "poured_date", "break_date", "dilate", "L", "A", "hp", "tp", 
        "hp_tp", "correction", "area", "load", "fc", "fc_MPa",
    )
    readonly_fields = (
        "poured_date", "break_date", "dilate", "L", "A", "hp", "tp", 
        "hp_tp", "correction", "area", "load", "fc", "fc_MPa",
    )
    extra = 0
    can_delete = False


class MasonryCompressionAdmin(admin.ModelAdmin):
    list_display = [ 
        "brick_type", "user", "name", "element_name", "code", "sampling_date",
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [MasonryAdmin,]

admin.site.register(MasonryCompression, MasonryCompressionAdmin)
