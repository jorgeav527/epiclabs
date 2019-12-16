from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('labs.urls', namespace="labs")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('students/', include('students.urls', namespace="students")),
    path('thesis/', include('thesis.urls', namespace="thesis")),
    path('construction/', include('construction.urls', namespace="construction")),
    path('reference-person/', include('reference_person.urls', namespace="reference_person")),
    path('tests-material/', include('tests_material.urls', namespace="tests_material")),
    path('tests-concrete/', include('tests_concrete.urls', namespace="tests_concrete")),
    path('tests-soil/', include('tests_soil.urls', namespace="tests_soil")),
]

admin.site.site_header = 'EPIC-labs Admin'       # default: "Django Administration"
admin.site.index_title = 'EPIC-labs Admin List'  # default: "Site administration"
admin.site.site_title = 'EPIC-labs Title'        # default: "Django site admin"
