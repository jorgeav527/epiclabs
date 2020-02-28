from django.urls import path

from . import views as labs_views

app_name = "labs"

urlpatterns = [
    # Generals Views
    path('', labs_views.home_view, name="home"),
    path('intro/', labs_views.intro_view, name="intro"),
    path('pricing/', labs_views.pricing_view, name="pricing"),
    path('contact/', labs_views.contact_view, name="contact"),
    # Laboratories Views
    path('tests-concrete/', labs_views.labs_concrete_view, name="concrete"),
    path('tests-material/', labs_views.labs_material_view, name="material"),
    path('tests-soil/', labs_views.labs_soil_view, name="soil"),
    # Sectors Views
        # Client Sector 
    path('sectors-client/', labs_views.sector_client_view, name="client"),
    path('sectors-client-info/', labs_views.sector_client_info_view, name="client_info"),
    path('sectors-client-equips-concrete/', labs_views.client_equips_concrete_view, name="client_equips_concrete"),
    path('sectors-client-equips-material/', labs_views.client_equips_material_view, name="client_equips_material"),
    path('sectors-client-equips-soil/', labs_views.client_equips_soil_view, name="client_equips_soil"),
        # Bach Sector
    path('sectors-bach/', labs_views.sector_bach_view, name="bach"),
    path('sectors-bach-info/', labs_views.sector_bach_info_view, name="bach_info"),
    path('sectors-bach-equips-concrete/', labs_views.bach_equips_concrete_view, name="bach_equips_concrete"),
    path('sectors-bach-equips-material/', labs_views.bach_equips_material_view, name="bach_equips_material"),
    path('sectors-bach-equips-soil/', labs_views.bach_equips_soil_view, name="bach_equips_soil"),
        # Student Sector
    path('sectors-student/', labs_views.sector_student_view, name="student"),
    path('sectors-student-info/', labs_views.sector_student_info_view, name="student_info"),
    path('sectors-student-equips-concrete/', labs_views.student_equips_concrete_view, name="student_equips_concrete"),
    path('sectors-student-equips-material/', labs_views.student_equips_material_view, name="student_equips_material"),
    path('sectors-student-equips-soil/', labs_views.student_equips_soil_view, name="student_equips_soil"),
        # General Sector
            # Info
    path('general/', labs_views.general_view, name="general"),
    path('general-personal/', labs_views.general_personal_view, name="general_personal"),
    path('general-clients/', labs_views.general_clients_view, name="general_clients"),
    path('general-ref-per/', labs_views.general_ref_per_view, name="general_ref_per"),
    path('general-construction/', labs_views.general_construction_view, name="general_construction"),
    path('general-bach/', labs_views.general_bach_view, name="general_bach"),
    path('general-thesis/', labs_views.general_thesis_view, name="general_thesis"),
    path('general-student/', labs_views.general_student_view, name="general_student"),
    path('general-equips/', labs_views.general_equips_view, name="general_equips"),
            # Info Tests Concrete
    path('general-diamond-pice-break/', labs_views.general_diamond_pice_break, name="general_diamond_pice_break"),
    path('general-pice-break/', labs_views.general_pice_break, name="general_pice_break"),
    path('general-prism-break/', labs_views.general_prism_break, name="general_prism_break"),
            # Info Tests Material
    path('general-brick-type/', labs_views.general_brick_type, name="general_brick_type"),
    path('general-masonry-compression/', labs_views.general_masonry_compression, name="general_masonry_compression"),
    path('general-wood-compression/', labs_views.general_wood_compression, name="general_wood_compression"),
            # Info Tests Soil
    path('general-equivalent/', labs_views.general_equivalent, name="general_equivalent"),
    path('general-fine-material/', labs_views.general_fine_material, name="general_fine_material"),
    path('general-granulometric-global/', labs_views.general_granulometric_global, name="general_granulometric_global"),
    path('general-limit/', labs_views.general_limit, name="general_limit"),
    path('general-moisture-content/', labs_views.general_moisture_content, name="general_moisture_content"),
    path('general-proctor-m/', labs_views.general_proctor_m, name="general_proctor_m"),
    path('general-sand-cone/', labs_views.general_sand_cone, name="general_sand_cone"),
    path('general-specific_gravity/', labs_views.general_specific_gravity, name="general_specific_gravity"),
]

