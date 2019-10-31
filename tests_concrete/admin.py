from django.contrib import admin

# Register your models here.
from .models import *

class PiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "poured_data", "break_data", "duration", "diameter_esp", "diameter_1", "diameter_2", "area", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(PiceBreak, PiceBreakAdmin)


class GroutDiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "poured_data", "break_data", "duration", "d_1", "d_2", "area", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(GroutDiceBreak, GroutDiceBreakAdmin)


class PaverBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "poured_data", "break_data", "duration", "d_1", "d_2", "area", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(PaverBreak, PaverBreakAdmin)


class LimeDiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "poured_data", "break_data", "duration", "d_1", "d_2", "area", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(LimeDiceBreak, LimeDiceBreakAdmin)


class LimePiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "poured_data", "break_data", "duration", "diameter_1", "diameter_2", "area", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(LimePiceBreak, LimePiceBreakAdmin)


class DiamondPiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "extraction_data", "break_data", "duration", "D",  "L", "factor_ld", "correction", "area",  
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(DiamondPiceBreak, DiamondPiceBreakAdmin)