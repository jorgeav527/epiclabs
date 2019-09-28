from django.contrib import admin

from .models import *

# Register your models here.

class GroutDiceBreakAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'edad', 'code', 'area', 'fc', 'fc_175', 'fc_210', 'fc_280',]

admin.site.register(GroutDiceBreak, GroutDiceBreakAdmin)
