from django.urls import path

from . import views as tests_soil_views

app_name = "tests_soil"

urlpatterns = [
    # General views Concrete
    path('info/', tests_soil_views.tests_soil_info_view, name="info"),
    path('equips/', tests_soil_views.tests_soil_equips_view, name="equips"),
    path('guides/', tests_soil_views.tests_soil_guides_view, name="guides"),
    path('teachers/', tests_soil_views.tests_soil_teachers_view, name="teachers"),
    # Limit CRUD and PDF
    path('limit/', tests_soil_views.limit_list, name="limit_list"),
    path('limit/create/', tests_soil_views.limit_create, name="limit_create"),
    path('limit/<int:id>/update/', tests_soil_views.limit_update, name="limit_update"),
    path('limit/<int:id>/detail/', tests_soil_views.limit_detail, name="limit_detail"),
    path('limit/<int:id>/delete/', tests_soil_views.limit_delete, name="limit_delete"),
    path('limit/<int:id>/pdf/', tests_soil_views.limit_pdf, name="limit_pdf"),
    # Liquid and Plastic CRUD
    path('liquid/save/<int:id>/', tests_soil_views.liquid_save, name="liquid_save"),
    path('plastic/save/<int:id>/', tests_soil_views.plastic_save, name="plastic_save"),
    # Fine Material CRUD and PDF
    path('fine-material/', tests_soil_views.fine_material_list, name="fine_material_list"),
    path('fine-material/create/', tests_soil_views.fine_material_create, name="fine_material_create"),
    path('fine-material/<int:id>/update/', tests_soil_views.fine_material_update, name="fine_material_update"),
    path('fine-material/<int:id>/detail/', tests_soil_views.fine_material_detail, name="fine_material_detail"),
    path('fine-material/<int:id>/delete/', tests_soil_views.fine_material_delete, name="fine_material_delete"),
    path('fine-material/<int:id>/pdf/', tests_soil_views.fine_material_pdf, name="fine_material_pdf"),
]