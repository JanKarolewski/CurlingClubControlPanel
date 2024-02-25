from rest_framework import generics, permissions, serializers
from events.models import Venue
from members.models import Club, Reservation, VenueTrack


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class VenueTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueTrack
        fields = '__all__'
