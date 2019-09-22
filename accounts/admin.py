from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_student', 'is_teacher', 'is_client', 'is_bach', 'is_admin', 'is_staff']
    
admin.site.register(User, UserAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ['course',]

admin.site.register(Course, CourseAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category',]

admin.site.register(Category, CategoryAdmin)


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['dni', 'codigo',]

admin.site.register(StudentProfile, StudentProfileAdmin)


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['dni', 'codigo',]

admin.site.register(TeacherProfile, TeacherProfileAdmin)


class BachProfileAdmin(admin.ModelAdmin):
    list_display = ['thesis_name', 'dni', 'codigo',]

admin.site.register(BachProfile, StudentProfileAdmin)


class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['long_name', 'ruc',]

admin.site.register(ClientProfile, ClientProfileAdmin)


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['staff', 'dni', 'codigo',]

admin.site.register(AdminProfile, AdminProfileAdmin)
