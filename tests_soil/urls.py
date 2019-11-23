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
    # Equivalent CRUD and PDF
    path('equivalent/', tests_soil_views.equivalent_list, name="equivalent_list"),
    path('equivalent/create/', tests_soil_views.equivalent_create, name="equivalent_create"),
    path('equivalent/<int:id>/update/', tests_soil_views.equivalent_update, name="equivalent_update"),
    path('equivalent/<int:id>/detail/', tests_soil_views.equivalent_detail, name="equivalent_detail"),
    path('equivalent/<int:id>/delete/', tests_soil_views.equivalent_delete, name="equivalent_delete"),
    path('equivalent/<int:id>/pdf/', tests_soil_views.equivalent_pdf, name="equivalent_pdf"),
    # Equiv CRUD
    path('equiv/save/<int:id>/', tests_soil_views.equiv_save, name="equiv_save"),
    # Proctor M CRUD and PDF
    path('proctor-m/', tests_soil_views.proctor_m_list, name="proctor_m_list"),
    path('proctor-m/create/', tests_soil_views.proctor_m_create, name="proctor_m_create"),
    path('proctor-m/<int:id>/update/', tests_soil_views.proctor_m_update, name="proctor_m_update"),
    path('proctor-m/<int:id>/detail/', tests_soil_views.proctor_m_detail, name="proctor_m_detail"),
    path('proctor-m/<int:id>/delete/', tests_soil_views.proctor_m_delete, name="proctor_m_delete"),
    path('proctor-m/<int:id>/pdf/', tests_soil_views.proctor_m_pdf, name="proctor_m_pdf"),
    # Density CRUD
    path('density/save/<int:id>/', tests_soil_views.density_save, name="density_save"),
    path('saturation/save/<int:id>/', tests_soil_views.saturation_save, name="saturation_save"),
    path('correction/save/<int:id>/', tests_soil_views.correction_save, name="correction_save"),
    # Moisture Content CRUD and PDF
    path('moisture-content/', tests_soil_views.moisture_content_list, name="moisture_content_list"),
    path('moisture-content/create/', tests_soil_views.moisture_content_create, name="moisture_content_create"),
    path('moisture-content/<int:id>/update/', tests_soil_views.moisture_content_update, name="moisture_content_update"),
    path('moisture-content/<int:id>/detail/', tests_soil_views.moisture_content_detail, name="moisture_content_detail"),
    path('moisture-content/<int:id>/delete/', tests_soil_views.moisture_content_delete, name="moisture_content_delete"),
    path('moisture-content/<int:id>/pdf/', tests_soil_views.moisture_content_pdf, name="moisture_content_pdf"),
    # Moisture Material CRUD
    path('moisture-material/save/<int:id>/', tests_soil_views.moisture_material_save, name="moisture_material_save"),
    # Specific Gravity CRUD and PDF
    path('specific-gravity/', tests_soil_views.specific_gravity_list, name="specific_gravity_list"),
    path('specific-gravity/create/', tests_soil_views.specific_gravity_create, name="specific_gravity_create"),
    path('specific-gravity/<int:id>/update/', tests_soil_views.specific_gravity_update, name="specific_gravity_update"),
    path('specific-gravity/<int:id>/detail/', tests_soil_views.specific_gravity_detail, name="specific_gravity_detail"),
    path('specific-gravity/<int:id>/delete/', tests_soil_views.specific_gravity_delete, name="specific_gravity_delete"),
    path('specific-gravity/<int:id>/pdf/', tests_soil_views.specific_gravity_pdf, name="specific_gravity_pdf"),
    # Fraction Pass and Retained CRUD
    path('fraction-pass/save/<int:id>/', tests_soil_views.fraction_pass_save, name="fraction_pass_save"),
    path('fraction-retained/save/<int:id>/', tests_soil_views.fraction_retained_save, name="fraction_retained_save"),
    # Granulometric Global CRUD and PDF
    path('granulometric-global/', tests_soil_views.granulometric_global_list, name="granulometric_global_list"),
    path('granulometric-global/create/', tests_soil_views.granulometric_global_create, name="granulometric_global_create"),
    path('granulometric-global/<int:id>/update/', tests_soil_views.granulometric_global_update, name="granulometric_global_update"),
    path('granulometric-global/<int:id>/detail/', tests_soil_views.granulometric_global_detail, name="granulometric_global_detail"),
    path('granulometric-global/<int:id>/delete/', tests_soil_views.granulometric_global_delete, name="granulometric_global_delete"),
    path('granulometric-global/<int:id>/pdf/', tests_soil_views.granulometric_global_pdf, name="granulometric_global_pdf"),
]