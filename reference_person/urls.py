from django.urls import path

from . import views as reference_person_views

app_name = "reference_person"

urlpatterns = [
    path('reference-person-create/', reference_person_views.reference_person_create, name="reference_person_create"),
    path('reference-person-update/<int:id>/', reference_person_views.reference_person_update, name="reference_person_update"),
    path('reference-person-delete/<int:id>/', reference_person_views.reference_person_delete, name="reference_person_delete"),
    # Ajax request Jquery
    path('ajax/reference_person/', reference_person_views.load_reference_person , name='ajax_reference_person'),
]