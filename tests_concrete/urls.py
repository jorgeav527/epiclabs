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
    path('pice-break/', tests_concrete_views.pice_break_list_view, name="pice_break_list"),
    path('pice-break/create/', tests_concrete_views.pice_break_create , name="pice_break_create"),
    path('pice-break/<int:id>/update/', tests_concrete_views.pice_break_update , name="pice_break_update"),
    path('pice-break/<int:id>/detail/', tests_concrete_views.pice_break_detail, name="pice_break_detail"),
    path('pice-break/<int:id>/delete/', tests_concrete_views.pice_break_delete , name="pice_break_delete"),
    path('pice-break/<int:id>/pdf/', tests_concrete_views.pice_break_pdf, name="pice_break_pdf"),
]