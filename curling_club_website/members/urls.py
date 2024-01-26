from django.urls import path, include

from api.views import ClubViewSet
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register-user'),
    path('register_club', views.register_club, name='register-club'),
    path('club_info_panel/<int:club>', views.club_info_panel, name='club-info-panel'),
    path('club_admin_panel/<int:pk>', views.ClubView.as_view(), name='club-admin-panel'),
    path('club_members_list/', views.MembersClubView.as_view(), name='club-members-panel'),
    path('profile_panel', views.profile_panel, name='profile-panel'),
    path('update_user', views.update_user, name='update-user'),
    path('update_profile', views.update_profile, name='update-profile'),
]
