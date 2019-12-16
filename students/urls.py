from django.urls import path

from . import views as student_views

app_name = "students"

urlpatterns = [
    path('student-group-save/<int:id>/', student_views.student_group_save, name="student_group_save"),
]