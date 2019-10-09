from django.urls import path

from . import views as tests_material_views

app_name = "tests_material"

urlpatterns = [
    path('info/', tests_material_views.tests_materials_info_view, name="info"),
    path('dice-break/', tests_material_views.grout_dice_break_list_view, name="dice_break_list"),
    path('dice-break/create/', tests_material_views.grout_dice_break_create, name="dice_break_create"),
    path('dice-break/<int:id>/update/', tests_material_views.grout_dice_brake_update, name="dice_break_update"),
    path('dice-break/<int:id>/delete/', tests_material_views.grout_dice_brake_delete, name="dice_break_delete"),
    path('dice-break/<int:id>/delail/', tests_material_views.grout_dice_brake_detail, name="dice_break_detail"),
    path('dice-break/<int:id>/pdf/', tests_material_views.grout_dice_brake_pdf, name="dice_break_pdf"),
]