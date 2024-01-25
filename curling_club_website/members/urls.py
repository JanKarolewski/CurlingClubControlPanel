from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register-user'),
    path('register_club', views.register_club, name='register-club'),
    path('club_info_panel/<int:club_id>', views.club_info_panel, name='club-info-panel'),
    path('profile_panel', views.profile_panel, name='profile-panel'),
    path('update_user', views.update_user, name='update-user'),
    path('update_profile', views.update_profile, name='update-profile'),
]
