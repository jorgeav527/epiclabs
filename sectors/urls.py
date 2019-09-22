from django.urls import path

from . import views as sectors_views

app_name = "sectors"

urlpatterns = [
    path('client/', sectors_views.sector_client_view, name="client"),
    path('student/', sectors_views.sector_student_view , name="student"),
    path('thesis/', sectors_views.sector_thesis_view, name="thesis"),
]
