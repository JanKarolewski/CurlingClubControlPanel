from rest_framework import generics, permissions, serializers
from events.models import Venue
from members.models import Club, Reservation, VenueTrack, Profile


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


class FilterForProfileSerializer(serializers.ModelSerializer):
    def get_user_name(self, obj):
        return obj.user.username

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    username = serializers.SerializerMethodField("get_user_name")
    first_name = serializers.SerializerMethodField("get_first_name")
    last_name = serializers.SerializerMethodField("get_last_name")

    class Meta:
        model = Profile

        fields = ('first_name', 'username', 'last_name')
        read_only_fields = ('id',)
