from django.urls import path

from . import views as tests_material_views

app_name = "tests_material"

urlpatterns = [
    # General views Concrete
    path('info/', tests_material_views.tests_material_info_view, name="info"),
    path('equips/', tests_material_views.tests_material_equips_view, name="equips"),
    path('guides/', tests_material_views.tests_material_guides_view, name="guides"),
    path('teachers/', tests_material_views.tests_material_teachers_view, name="teachers"),
]