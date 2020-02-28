from django.urls import path

from . import views as student_views

app_name = "students"

urlpatterns = [
    path('student-create/', student_views.student_create, name="student_create"),
    path('student-update/<int:id>/', student_views.student_update, name="student_update"),
    path('student-delete/<int:id>/', student_views.student_delete, name="student_delete"),
]