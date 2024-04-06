from django.contrib import admin
from django.contrib.auth.models import User

from members.models import Club, Profile, VenueIceOpenHours, Reservation, VenueTrack, FriendRequest
from .models import Venue, Event, Post

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(Club)
admin.site.register(Profile)
# admin.site.register(Reservation)
admin.site.register(VenueIceOpenHours)
admin.site.register(VenueTrack)
admin.site.register(FriendRequest)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('title', 'from_hour', 'to_hour')
    ordering = ('-from_hour',)


# @admin.register(Venue)
# class VenueAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address', 'zip_code')
#     ordering = ('name',)
#     search_fields = ('name', 'address', 'zip_code')
#
#
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     fields = (('name', 'venue'), 'event_date', 'description', 'manager')
#     list_display = ('name', 'event_date')
#     list_filter = ('event_date', 'venue')
#     ordering = ('-event_date',)
