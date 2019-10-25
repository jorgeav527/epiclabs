from django.urls import path

from . import views as accounts_views

app_name = "construction"

urlpatterns = [
    path('construction-create/', accounts_views.construction_create, name="construction_create"),
    path('construction-update/<int:id>/', accounts_views.construction_update, name="construction_update"),
    path('construction-delete/<int:id>/', accounts_views.construction_delete, name="construction_delete"),
]