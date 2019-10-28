from django.contrib import admin

from .models import *

# Register your models here.
class ReferencePersonAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'dni', 'phone', 'client_profile']

admin.site.register(ReferencePerson, ReferencePersonAdmin)
