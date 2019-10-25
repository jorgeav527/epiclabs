from django.urls import path

from . import views as accounts_views

app_name = "reference_person"

urlpatterns = [
    path('reference-person-create/', accounts_views.reference_person_create, name="reference_person_create"),
    path('reference-person-update/<int:id>/', accounts_views.reference_person_update, name="reference_person_update"),
    path('reference-person-delete/<int:id>/', accounts_views.reference_person_delete, name="reference_person_delete"),
]