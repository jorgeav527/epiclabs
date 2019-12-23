from django.contrib import admin

# Register your models here.
from .models import *

class PiceAdmin(admin.TabularInline):
    model = Pice
    fields = ( 
        "poured_date", "element_name", "break_date", "dilate", "D_1", "D_2", "area", "load", 
        "fc", "fc_MPa", "fc_175", "fc_210", "fc_280",
    )
    readonly_fields = (
        "poured_date", "element_name", "break_date", "dilate", "D_1", "D_2", "area", "load", 
        "fc", "fc_MPa", "fc_175", "fc_210", "fc_280",
    )
    extra = 0
    can_delete = False

class PiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "code", "pice_type", "fc_esp", "sampling_date", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [PiceAdmin,]

admin.site.register(PiceBreak, PiceBreakAdmin)


class PrismAdmin(admin.TabularInline):
    model = Prism
    fields = ( 
        "poured_date", "element_name", "break_date", "dilate", "D_1", "D_2", "area", "load", 
        "fc", "fc_MPa", "fc_175", "fc_210", "fc_280",
    )
    readonly_fields = (
        "poured_date", "element_name", "break_date", "dilate", "D_1", "D_2", "area", "load", 
        "fc", "fc_MPa", "fc_175", "fc_210", "fc_280",
    )
    extra = 0
    can_delete = False

class PrismBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "code", "prism_type", "fc_esp", "sampling_date", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [PrismAdmin,]

admin.site.register(PrismBreak, PrismBreakAdmin)


class DiamondPice(admin.TabularInline):
    model = DiamondPice
    fields = ( 
        'extraction_date', 'break_date', 'dilate', 'element_name', 'D', 'L', 
        'factor_ld', 'area', 'correction', 'load', 'fc', 'fc_MPa', 'fc_175', 'fc_210', 'fc_280',
    )
    readonly_fields = (
        'extraction_date', 'break_date', 'dilate', 'element_name', 'D', 'L', 
        'factor_ld', 'area', 'correction', 'load', 'fc', 'fc_MPa', 'fc_175', 'fc_210', 'fc_280',
    )
    extra = 0
    can_delete = False


class DiamondPiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "code", "fc_esp", "sampling_date", 
        "reference_person", "construction", "created", "updated",
    ]
    inlines = [DiamondPice,]

admin.site.register(DiamondPiceBreak, DiamondPiceBreakAdmin)