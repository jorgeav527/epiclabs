from django.urls import path

from . import views as construction_views

app_name = "construction"

urlpatterns = [
    path('construction-create/', construction_views.construction_create, name="construction_create"),
    path('construction-update/<int:id>/', construction_views.construction_update, name="construction_update"),
    path('construction-delete/<int:id>/', construction_views.construction_delete, name="construction_delete"),
    # Ajax request Jquery
    path('ajax/construction/', construction_views.load_construction, name='ajax_construction'),
]