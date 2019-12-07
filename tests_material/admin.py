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
         "length", "width", "high", "volume_brick", "bar_500", "sc", "su", "bar", 
         "volume_void", "volume_real", "void_percentage", "weight", "density",
    )
    readonly_fields = (
         "length", "width", "high", "volume_brick", "bar_500", "sc", "su", "bar", 
         "volume_void", "volume_real", "void_percentage", "weight", "density",
    )
    extra = 0
    can_delete = False


class SuctionAdmin(admin.TabularInline):
    model = Suction
    fields = (
        "nomal_weight", "dry_weight", "diff_weight", "length", "width", "face_area", "bar_200", 
        "face_wet_weight", "face_wet_weight_correction",
    )
    readonly_fields = (
        "nomal_weight", "dry_weight", "diff_weight", "length", "width", "face_area", "bar_200", 
        "face_wet_weight", "face_wet_weight_correction",
    )
    extra = 0
    can_delete = False


class AbsSatuCoeffAdmin(admin.TabularInline):
    model = AbsSatuCoeff
    fields = (
        "dry_weight", "wet_weight_cool_24", "wet_weight_hot_24", "wet_weight_hot_5", 
        "abs_brick", "abs_max_brick", "coeff_sat",
    )
    readonly_fields = (
        "dry_weight", "wet_weight_cool_24", "wet_weight_hot_24", "wet_weight_hot_5", 
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
