from django.urls import path

from . import views as tests_material_views

app_name = "tests_material"

urlpatterns = [
    path('info/', tests_material_views.tests_materials_info_view, name="info"),
    path('dice-break/', tests_material_views.grout_dice_break_view, name="dice_break"),
]