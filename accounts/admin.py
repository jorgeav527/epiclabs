from django.contrib import admin

# Register your models here.
from .models import *
from students.models import StudentGroup

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_group', 'is_teacher', 'is_client', 'is_bach', 'is_admin', 'is_staff']
    
admin.site.register(User, UserAdmin)


class StudentGroupAdmin(admin.TabularInline):
    model = StudentGroup
    fields = ( 
        'full_name', 'codigo', 'email', 'phone', 'group_profile'
    )
    readonly_fields = (
        'full_name', 'codigo', 'email', 'phone', 'group_profile'
    )
    extra = 0
    can_delete = False


class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'active', 'group_name', 'created', 'updated',]
    inlines = [StudentGroupAdmin,]

admin.site.register(GroupProfile, GroupProfileAdmin)


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'dni', 'codigo', 'active']

admin.site.register(TeacherProfile, TeacherProfileAdmin)


class BachProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dni', 'codigo', 'active']

admin.site.register(BachProfile, BachProfileAdmin)


class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'long_name', 'direction', 'ruc', 'phone', 'active']

admin.site.register(ClientProfile, ClientProfileAdmin)


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'staff', 'dni', 'codigo', 'active']

admin.site.register(AdminProfile, AdminProfileAdmin)
