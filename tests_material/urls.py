from django.urls import path

from . import views as tests_material_views

app_name = "tests_material"

urlpatterns = [
    # General views Concrete
    path('info/', tests_material_views.tests_material_info_view, name="info"),
    path('equips/', tests_material_views.tests_material_equips_view, name="equips"),
    path('guides/', tests_material_views.tests_material_guides_view, name="guides"),
    path('teachers/', tests_material_views.tests_material_teachers_view, name="teachers"),
    # Brick Type CRUD and PDF
    path('brick-type/', tests_material_views.brick_type_list, name="brick_type_list"),
    path('brick-type/create/', tests_material_views.brick_type_create, name="brick_type_create"),
    path('brick-type/<int:id>/update/', tests_material_views.brick_type_update, name="brick_type_update"),
    path('brick-type/<int:id>/detail/', tests_material_views.brick_type_detail, name="brick_type_detail"),
    path('brick-type/<int:id>/delete/', tests_material_views.brick_type_delete, name="brick_type_delete"),
    path('brick-type/<int:id>/pdf/', tests_material_views.brick_type_pdf, name="brick_type_pdf"),
        #  CRUD
    path('variation-dimensions/save/<int:id>/', tests_material_views.variation_dimensions_save , name="variation_dimensions_save"),
    path('warping/save/<int:id>/', tests_material_views.warping_save , name="warping_save"),
    path('density-voids/save/<int:id>/', tests_material_views.density_voids_save , name="density_voids_save"),
    path('suction/save/<int:id>/', tests_material_views.suction_save , name="suction_save"),
    path('abs-satu-coeff/save/<int:id>/', tests_material_views.abs_satu_coeff_save , name="abs_satu_coeff_save"),
    path('compretion-brick/save/<int:id>/', tests_material_views.compretion_brick_save , name="compretion_brick_save"),
    # Wood Compression CRUD and PDF
    path('wood-compression/', tests_material_views.wood_compression_list, name="wood_compression_list"),
    path('wood-compression/create/', tests_material_views.wood_compression_create, name="wood_compression_create"),
    path('wood-compression/<int:id>/update/', tests_material_views.wood_compression_update, name="wood_compression_update"),
    path('wood-compression/<int:id>/detail/', tests_material_views.wood_compression_detail, name="wood_compression_detail"),
    path('wood-compression/<int:id>/delete/', tests_material_views.wood_compression_delete, name="wood_compression_delete"),
    path('wood-compression/<int:id>/pdf/', tests_material_views.wood_compression_pdf, name="wood_compression_pdf"),
        #  CRUD
    path('parallel-perpendicular/save/<int:id>/', tests_material_views.parallel_perpendicular_save , name="parallel_perpendicular_save"),
    # Masonry Compression CRUD and PDF
    path('masonry-compression/', tests_material_views.masonry_compression_list, name="masonry_compression_list"),
    path('masonry-compression/create/', tests_material_views.masonry_compression_create, name="masonry_compression_create"),
    path('masonry-compression/<int:id>/update/', tests_material_views.masonry_compression_update, name="masonry_compression_update"),
    path('masonry-compression/<int:id>/detail/', tests_material_views.masonry_compression_detail, name="masonry_compression_detail"),
    path('masonry-compression/<int:id>/delete/', tests_material_views.masonry_compression_delete, name="masonry_compression_delete"),
    path('masonry-compression/<int:id>/pdf/', tests_material_views.masonry_compression_pdf, name="masonry_compression_pdf"),
        #  CRUD
    path('masonry/save/<int:id>/', tests_material_views.masonry_save , name="masonry_save"),
]