from django.urls import path

from . import views as labs_views

app_name = "labs"

urlpatterns = [
    # Generals Views
    path('', labs_views.home_view, name="home"),
    path('pricing/', labs_views.pricing_view, name="pricing"),
    path('contact/', labs_views.contact_view, name="contact"),
    # Laboratories Views
    path('tests-concrete/', labs_views.labs_concrete_view, name="concrete"),
    path('tests-material/', labs_views.labs_material_view, name="material"),
    path('tests-soil/', labs_views.labs_soil_view, name="soil"),
    # Sectors Views
        # Client Sector 
    path('sectors-client/', labs_views.sector_client_view, name="client"),
    path('sectors-client-info-clients/', labs_views.client_info_clients_view, name="client_info_clients"),
    path('sectors-client-info-ref-per/', labs_views.client_info_ref_per_view, name="client_info_ref_per"),
    path('sectors-client-info-construction/', labs_views.client_info_construction_view, name="client_info_construction"),
    path('sectors-client-equips-concrete/', labs_views.client_equips_concrete_view, name="client_equips_concrete"),
    path('sectors-client-equips-material/', labs_views.client_equips_material_view, name="client_equips_material"),
    path('sectors-client-equips-soil/', labs_views.client_equips_soil_view, name="client_equips_soil"),
    path('sectors-client-tests-concrete/', labs_views.client_tests_concrete_view, name="client_tests_concrete"),
    path('sectors-client-tests-material/', labs_views.client_tests_material_view, name="client_tests_material"),
    path('sectors-client-tests-soil/', labs_views.client_tests_soil_view, name="client_tests_soil"),
        # Bach Sector
    path('sectors-bach/', labs_views.sector_bach_view, name="bach"),
    path('sectors-bach-info/', labs_views.bach_info_view, name="bach_info"),
    path('sectors-bach-equips/', labs_views.bach_equips_view, name="bach_equips"),
    path('sectors-bach-personal/', labs_views.bach_personal_view, name="bach_personal"),
    path('sectors-bach-laboratorios/', labs_views.bach_laboratories_view, name="bach_laboratories"),
        # Student Sector
    path('sectors-student/', labs_views.sector_student_view, name="student"),
    path('sectors-student-info/', labs_views.student_info_view, name="student_info"),
    path('sectors-student-equips/', labs_views.student_equips_view, name="student_equips"),
    path('sectors-student-personal/', labs_views.student_personal_view, name="student_personal"),
    path('sectors-student-laboratorios/', labs_views.student_laboratories_view, name="student_laboratories"),
        # General Sector
    path('general/', labs_views.general_view, name="general"),
    path('general-personal/', labs_views.general_personal_view, name="general_personal"),
    path('general-equips/', labs_views.general_equips_view, name="general_equips"),
]

