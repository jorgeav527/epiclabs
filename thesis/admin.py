from django.contrib import admin

from .models import *
# Register your models here.
class ThesisAdmin(admin.ModelAdmin):
    list_display = ['title', 'line', 'start_day', 'finish_day', 'bach_profile']

admin.site.register(Thesis, ThesisAdmin)


