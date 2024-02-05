from django.urls import path, include

from api.views import ClubViewSet
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # club administration
    path('register_club', views.register_club, name='register-club'),
    path('club_info_panel/<int:club>', views.club_info_panel, name='club-info-panel'),
    path('club_admin_panel/<int:pk>', views.ClubView.as_view(), name='club-admin-panel'),

    # user administration
    path('register_user', views.register_user, name='register-user'),
    path('club_members_list/', views.MembersClubView.as_view(), name='club-members-panel'),
    path('profile_panel', views.profile_panel, name='profile-panel'),
    path('update_user', views.update_user, name='update-user'),
    path('update_profile', views.update_profile, name='update-profile'),

    # ice reservation panel
    path('club-calendar-reservation-view', views.club_calendar_reservation_view, name='club-calendar-reservation-view'),
    path('club-ice-availability-schedule', views.club_ice_availability_schedule, name='club-ice-availability-schedule'),
    path('edit-ice-availability-schedule/<int:day_name>', views.edit_ice_availability_schedule,
         name='edit-ice-availability-schedule'),
    path('delete-ice-availability-schedule/<int:day_name>', views.delete_ice_availability_schedule,
         name='delete-ice-availability-schedule'),
    path('create-ice-reservation-for-user', views.create_ice_reservation_for_user,
         name='create-ice-reservation-for-user'),

]
