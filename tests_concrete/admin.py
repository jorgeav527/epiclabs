from django.contrib import admin

# Register your models here.
from .models import PiceBreak

class PiceBreakAdmin(admin.ModelAdmin):
    list_display = ["user", "edad", "area", "F", "fc_175", "fc_210", "fc_210", "created", "updated",]

admin.site.register(PiceBreak, PiceBreakAdmin)