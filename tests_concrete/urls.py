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
        # Pice CRUD
    path('pice/save/<int:id>/', tests_concrete_views.pice_save, name="pice_save"),    
    # Prism Break CRUD and PDF
    path('prism-break/', tests_concrete_views.prism_break_list, name="prism_break_list"),
    path('prism-break/create/', tests_concrete_views.prism_break_create , name="prism_break_create"),
    path('prism-break/<int:id>/update/', tests_concrete_views.prism_break_update , name="prism_break_update"),
    path('prism-break/<int:id>/detail/', tests_concrete_views.prism_break_detail, name="prism_break_detail"),
    path('prism-break/<int:id>/delete/', tests_concrete_views.prism_break_delete , name="prism_break_delete"),
    path('prism-break/<int:id>/pdf/', tests_concrete_views.prism_break_pdf, name="prism_break_pdf"),
        # Prism CRUD
    path('prism/save/<int:id>/', tests_concrete_views.prism_save, name="prism_save"),    
    # Diamond Pice Break CRUD and PDF
    path('diamond-pice-break/', tests_concrete_views.diamond_pice_break_list, name="diamond_pice_break_list"),
    path('diamond-pice-break/create/', tests_concrete_views.diamond_pice_break_create, name="diamond_pice_break_create"),
    path('diamond-pice-break/<int:id>/update/', tests_concrete_views.diamond_pice_break_update, name="diamond_pice_break_update"),
    path('diamond-pice-break/<int:id>/detail/', tests_concrete_views.diamond_pice_break_detail, name="diamond_pice_break_detail"),
    path('diamond-pice-break/<int:id>/delete/', tests_concrete_views.diamond_pice_break_delete , name="diamond_pice_break_delete"),
    path('diamond-pice-break/<int:id>/pdf/', tests_concrete_views.diamond_pice_break_pdf, name="diamond_pice_break_pdf"),
        # Prism CRUD
    path('diamond-pice/save/<int:id>/', tests_concrete_views.diamond_pice_save, name="diamond_pice_save"),    
]