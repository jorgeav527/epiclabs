from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_student', 'is_teacher', 'is_client', 'is_bach', 'is_admin', 'is_staff']
    
admin.site.register(User, UserAdmin)


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dni', 'codigo', 'active']

admin.site.register(StudentProfile, StudentProfileAdmin)


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'dni', 'codigo', 'active']

admin.site.register(TeacherProfile, TeacherProfileAdmin)


class BachProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dni', 'codigo', 'active']

admin.site.register(BachProfile, StudentProfileAdmin)


class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'long_name', 'direction', 'ruc', 'phone', 'active']

admin.site.register(ClientProfile, ClientProfileAdmin)


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'staff', 'dni', 'codigo', 'active']

admin.site.register(AdminProfile, AdminProfileAdmin)
