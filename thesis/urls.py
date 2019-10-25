from django.urls import path

from . import views as accounts_views

app_name = "thesis"

urlpatterns = [
    path('thesis-create/', accounts_views.thesis_create, name="thesis_create"),
    path('thesis-update/<int:id>/', accounts_views.thesis_update, name="thesis_update"),
    path('thesis-delete/<int:id>/', accounts_views.thesis_delete, name="thesis_delete"),
]