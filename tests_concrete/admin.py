from django.contrib import admin

# Register your models here.
from .models import PiceBreak

class PiceBreakAdmin(admin.ModelAdmin):
    list_display = [
        "user", "element", "code", "F", "fc_MPa", "fc_esp", "fc_175", "fc_210", "fc_210", 
        "poured_data", "break_data", "duration", "diameter_esp", "diameter_1", "diameter_2", "area", 
        "reference_person", "construction", "created", "updated",
    ]

admin.site.register(PiceBreak, PiceBreakAdmin)