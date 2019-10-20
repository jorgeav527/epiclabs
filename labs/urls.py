from django.urls import path

from . import views as labs_views

app_name = "labs"

urlpatterns = [
    path('', labs_views.labs_home_view, name="home"),
    path('tests-concrete/', labs_views.labs_concrete_view, name="concrete"),
    path('tests-material/', labs_views.labs_material_view, name="material"),
    path('tests-soil/', labs_views.labs_soil_view, name="soil"),

    path('pricing/', labs_views.pricing_view, name="pricing"),

    path('contact/', labs_views.contact_view, name="contact"),
]

