from django.urls import path

from . import views as tests_concrete_views

app_name = "tests_concrete"

urlpatterns = [
    # General views Concrete
    path('info/', tests_concrete_views.tests_concrete_info_view, name="info"),
    path('equips/', tests_concrete_views.tests_concrete_equips_view, name="equips"),
    path('guides/', tests_concrete_views.tests_concrete_guides_view, name="guides"),
    path('teachers/', tests_concrete_views.tests_concrete_teachers_view, name="teachers"),
    # Pice Break CRUD and PDF
    path('pice-break/', tests_concrete_views.pice_break_list, name="pice_break_list"),
    path('pice-break/create/', tests_concrete_views.pice_break_create , name="pice_break_create"),
    path('pice-break/<int:id>/update/', tests_concrete_views.pice_break_update , name="pice_break_update"),
    path('pice-break/<int:id>/detail/', tests_concrete_views.pice_break_detail, name="pice_break_detail"),
    path('pice-break/<int:id>/delete/', tests_concrete_views.pice_break_delete , name="pice_break_delete"),
    path('pice-break/<int:id>/pdf/', tests_concrete_views.pice_break_pdf, name="pice_break_pdf"),
    # Grout Dice Break CRUD and PDF
    path('grout-dice-break/', tests_concrete_views.grout_dice_break_list, name="grout_dice_break_list"),
    path('grout-dice-break/create/', tests_concrete_views.grout_dice_break_create, name="grout_dice_break_create"),
    path('grout-dice-break/<int:id>/update/', tests_concrete_views.grout_dice_break_update, name="grout_dice_break_update"),
    path('grout-dice-break/<int:id>/detail/', tests_concrete_views.grout_dice_break_detail, name="grout_dice_break_detail"),
    path('grout-dice-break/<int:id>/delete/', tests_concrete_views.grout_dice_break_delete , name="grout_dice_break_delete"),
    path('grout-dice-break/<int:id>/pdf/', tests_concrete_views.grout_dice_break_pdf, name="grout_dice_break_pdf"),
    # Paver Break CRUD and PDF
    path('paver-break/', tests_concrete_views.paver_break_list, name="paver_break_list"),
    path('paver-break/create/', tests_concrete_views.paver_break_create, name="paver_break_create"),
    path('paver-break/<int:id>/update/', tests_concrete_views.paver_break_update, name="paver_break_update"),
    path('paver-break/<int:id>/detail/', tests_concrete_views.paver_break_detail, name="paver_break_detail"),
    path('paver-break/<int:id>/delete/', tests_concrete_views.paver_break_delete , name="paver_break_delete"),
    path('paver-break/<int:id>/pdf/', tests_concrete_views.paver_break_pdf, name="paver_break_pdf"),
    # Lime Dice Break CRUD and PDF
    path('lime-dice-break/', tests_concrete_views.lime_dice_break_list, name="lime_dice_break_list"),
    path('lime-dice-break/create/', tests_concrete_views.lime_dice_break_create, name="lime_dice_break_create"),
    path('lime-dice-break/<int:id>/update/', tests_concrete_views.lime_dice_break_update, name="lime_dice_break_update"),
    path('lime-dice-break/<int:id>/detail/', tests_concrete_views.lime_dice_break_detail, name="lime_dice_break_detail"),
    path('lime-dice-break/<int:id>/delete/', tests_concrete_views.lime_dice_break_delete , name="lime_dice_break_delete"),
    path('lime-dice-break/<int:id>/pdf/', tests_concrete_views.lime_dice_break_pdf, name="lime_dice_break_pdf"),
    # Lime Pice Break CRUD and PDF
    path('lime-pice-break/', tests_concrete_views.lime_pice_break_list, name="lime_pice_break_list"),
    path('lime-pice-break/create/', tests_concrete_views.lime_pice_break_create, name="lime_pice_break_create"),
    path('lime-pice-break/<int:id>/update/', tests_concrete_views.lime_pice_break_update, name="lime_pice_break_update"),
    path('lime-pice-break/<int:id>/detail/', tests_concrete_views.lime_pice_break_detail, name="lime_pice_break_detail"),
    path('lime-pice-break/<int:id>/delete/', tests_concrete_views.lime_pice_break_delete , name="lime_pice_break_delete"),
    path('lime-pice-break/<int:id>/pdf/', tests_concrete_views.lime_pice_break_pdf, name="lime_pice_break_pdf"),
    # Diamond Pice Break CRUD and PDF
    path('diamond-pice-break/', tests_concrete_views.diamond_pice_break_list, name="diamond_pice_break_list"),
    path('diamond-pice-break/create/', tests_concrete_views.diamond_pice_break_create, name="diamond_pice_break_create"),
    path('diamond-pice-break/<int:id>/update/', tests_concrete_views.diamond_pice_break_update, name="diamond_pice_break_update"),
    path('diamond-pice-break/<int:id>/detail/', tests_concrete_views.diamond_pice_break_detail, name="diamond_pice_break_detail"),
    path('diamond-pice-break/<int:id>/delete/', tests_concrete_views.diamond_pice_break_delete , name="diamond_pice_break_delete"),
    path('diamond-pice-break/<int:id>/pdf/', tests_concrete_views.diamond_pice_break_pdf, name="diamond_pice_break_pdf"),
]