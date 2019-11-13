from django.contrib import admin

from .models import *

# Register your models here.

class LimitAdmin(admin.ModelAdmin):
    list_display = [
        "user", "pit", "layer", "code", "extraction_data", "done_data", "duration", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(Limit, LimitAdmin)


class LiquidAdmin(admin.ModelAdmin):
    list_display = [
        "bowl", "hit", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "water_weight", "moisture", "limit",
    ]

admin.site.register(Liquid, LiquidAdmin)


class PlasticAdmin(admin.ModelAdmin):
    list_display = [
        "bowl", "bowl_weight", "wet_weight", "dry_weight", 
        "water_weight", "water_weight", "moisture", "limit",
    ]

admin.site.register(Platic, PlasticAdmin)


class FineMaterialAdmin(admin.ModelAdmin):
    list_display = [
        "user", "pit", "layer", "code", "sampling_date", "done_date", "duration", 
        "bowl", "before_weight", "bowl_weight", "after_weight", "pass_weight", "fine", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(FineMaterial, FineMaterialAdmin)
