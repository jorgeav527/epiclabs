from django.contrib import admin

from .models import *
# Register your models here.

class ConstructionAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'start_day', 'finish_day', 'client_profile']

admin.site.register(Construction, ConstructionAdmin)
