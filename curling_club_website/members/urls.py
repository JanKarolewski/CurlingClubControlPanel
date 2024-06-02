from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # club administration
    path('register_club', views.register_club, name='register-club'),
    path('club_info_panel/<int:club>', views.club_info_panel, name='club-info-panel'),
    path('update_club_data', views.update_club_data, name='update-club-data'),
    path('club_admin_panel/<int:pk>', views.ClubView.as_view(), name='club-admin-panel'),
    path('club-members-reservation', views.ClubMembersReservation.as_view(), name='club-members-reservation'),
    path('panel-for-import-members', views.panel_for_import_members, name='panel-for-import-members'),
    path('add-file-with-club-members/', views.upload_file_with_members, name='add-file-with-club-members'),

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
    path('edit-venue-track/<int:track_id>', views.edit_venue_track, name='edit-venue-track'),
    path('delete-venue-track/<int:track_id>', views.delete_venue_track, name='delete-venue-track'),
    path('all-venues-list', views.all_venues_list, name='all-venues-list'),
    path('add-profile-for-work-group/<int:venue_id>', views.add_profile_for_work_group, name='add-profile-for-work-group'),
    path('venue-reservation-list', views.VenueReservation.as_view(), name='venue-reservation-list'),


    # user administration
    path('register_user', views.register_user, name='register-user'),
    path('club_members_list/', views.MembersClubView.as_view(), name='club-members-panel'),
    path('profile_panel', views.profile_panel, name='profile-panel'),
    path('update_user', views.update_user, name='update-user'),
    path('update_profile', views.update_profile, name='update-profile'),
    path('user-reservations-list', views.user_reservations_list, name='user-reservations-list'),
    path('user-friends-list', views.user_friends_list, name='user-friends-list'),
    path('send-friend-request', views.send_friend_request, name='send-friend-request'),
    path('accept-friend-request', views.accept_friend_request, name='accept-friend-request'),
    path('remove-from-friend-list', views.remove_from_friend_list, name='remove-from-friend-list'),
    path('append-attendees-to-reservation', views.append_attendees_to_reservation, name='append-attendees-to-reservation'),

    # ice reservation calendar
    # path for calendar as normal user
    path('create-ice-reservation/<int:venue_id>', views.create_ice_reservation,
         name='create-ice-reservation'),
    # path for calendar for administrators
    path('create-ice-reservation-for-user/<int:venue_id>', views.create_ice_reservation_for_user,
         name='create-ice-reservation-for-user'),
    # path('all_club_ice_reservation/', views.all_club_ice_reservation, name='all_club_ice_reservation'),
    # path('add_club_ice_reservation/', views.add_club_ice_reservation, name='add_club_ice_reservation'),
]
