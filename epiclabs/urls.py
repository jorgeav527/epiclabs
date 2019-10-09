from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('labs.urls', namespace="labs")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('tests-material/', include('tests_material.urls', namespace="tests_material")),
    path('tests-concrete/', include('tests_concrete.urls', namespace="tests_concrete")),
]

admin.site.site_header = 'EPIC-labs Admin'       # default: "Django Administration"
admin.site.index_title = 'EPIC-labs Admin List'  # default: "Site administration"
admin.site.site_title = 'EPIC-labs Title'        # default: "Django site admin"
