from django.contrib import admin

# Register your models here.
from .models import *

class EquipAdmin(admin.ModelAdmin):
    list_display = ["name", "shop_day", "last_maintenance_day", "next_maintenance_day", "maintenance_done", "use",]

admin.site.register(Equip, EquipAdmin)

