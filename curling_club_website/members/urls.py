from django.urls import path, include, re_path

from api.views import ClubViewSet
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # club administration
    path('register_club', views.register_club, name='register-club'),
    path('club_info_panel/<int:club>', views.club_info_panel, name='club-info-panel'),
    path('club_admin_panel/<int:pk>', views.ClubView.as_view(), name='club-admin-panel'),

    # venue (Ice Arena) administration
    path('venue_info_panel', views.venue_info_panel, name='venue-info-panel'),
    path('venue-calendar-reservation-view', views.venue_calendar_reservation_view,
         name='venue-calendar-reservation-view'),
    path('venue-ice-availability-schedule', views.venue_ice_availability_schedule,
         name='venue-ice-availability-schedule'),
    path('edit-ice-availability-schedule/<int:day_name>', views.edit_ice_availability_schedule,
         name='edit-ice-availability-schedule'),
    path('delete-ice-availability-schedule/<int:day_name>', views.delete_ice_availability_schedule,
         name='delete-ice-availability-schedule'),
    path('venue-tracks-view', views.venue_tracks_view, name='venue-tracks-view'),
    path('venue-track-form', views.venue_track_form, name='venue-track-form'),
    path('edit-venue-track/<int:track_id>', views.edit_venue_track,
         name='edit-venue-track'),
    path('delete-venue-track/<int:track_id>', views.delete_venue_track,
         name='delete-venue-track'),

    # user administration
    path('register_user', views.register_user, name='register-user'),
    path('club_members_list/', views.MembersClubView.as_view(), name='club-members-panel'),
    path('profile_panel', views.profile_panel, name='profile-panel'),
    path('update_user', views.update_user, name='update-user'),
    path('update_profile', views.update_profile, name='update-profile'),

    # ice reservation calendar
    re_path(r'create-ice-reservation-for-user/(?:year-(?P<year>[0-9]+)/)?$',
            views.create_ice_reservation_for_user, name='create-ice-reservation-for-user'),
    # path('all_club_ice_reservation/', views.all_club_ice_reservation, name='all_club_ice_reservation'),
    # path('add_club_ice_reservation/', views.add_club_ice_reservation, name='add_club_ice_reservation'),
]
