from django.contrib import admin

from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'codigo', 'email', 'phone', 'group_profile']

admin.site.register(Student, StudentAdmin)
