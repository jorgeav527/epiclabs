from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Equip)
class EquipAdmin(ImportExportModelAdmin):
    list_display = ["name", "shop_day", "last_maintenance_day", "next_maintenance_day", "maintenance_done", "use",]


