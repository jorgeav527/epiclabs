from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/student/', accounts_views.register_student , name="register_student"),
    path('register/student/profile/', accounts_views.profile_student , name="profile_student"),
    path('register/bach/', accounts_views.register_bach , name="register_bach"),
    path('register/bach/profile/', accounts_views.profile_bach , name="profile_bach"),
    path('register/teacher/', accounts_views.register_teacher , name="register_teacher"),
    path('register/teacher/profile/', accounts_views.profile_teacher , name="profile_teacher"),
    path('register/client/', accounts_views.register_client , name="register_client"),
    path('register/client/profile/', accounts_views.profile_client , name="profile_client"),
    path('register/admin/', accounts_views.register_admin , name="register_admin"),
    path('register/admin/profile/', accounts_views.profile_admin , name="profile_admin"),
]