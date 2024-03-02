from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from members.models import Club, Reservation, VenueTrack
from .serializers import VenueSerializer, ClubSerializer, ReservationSerializer, VenueTrackSerializer
from events.models import Venue

from datetime import datetime

# class VenueViewSet1(generics.CreateAPIView):
#     queryset = Venue.objects.all()
#     serializer_class = VenueSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     http_method_names = ['post']


class Logout(APIView):
    @staticmethod
    def get(request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class VenueViewSet2(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        # self.queryset = self.queryset.filter(club=self.request.user.profile.club)
        # Get all club reservation for calendar in 3 cases (your reservation, or if admin venue -> all reservation, 3 case whec club admin -> to do )

        venue = self.request.GET.get('venue', None)
        venue_info = Venue.objects.get(id=venue)
        self.queryset = self.queryset.filter(venue=venue)
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        user = self.request.user.profile

        if venue_info.administrator.pk == user.pk:
            # ToDo or user is venue worker
            is_venue_admin_or_worker = True
            print(is_venue_admin_or_worker)
        else:
            self.queryset = self.queryset.filter(attendees__in=[user.pk])
            self.queryset = self.queryset.filter(creator=user.pk)

        if start:
            start = datetime.strptime(start, "%Y-%m-%d")
            self.queryset = self.queryset.filter(reservation_date__gte=start)
        if end:
            end = datetime.strptime(end, "%Y-%m-%d")
            self.queryset = self.queryset.filter(reservation_date__lte=end)
        return self.queryset

    @action(detail=False, methods=['GET'])
    def reservation_for_calendar(self, request):
        # Get all club reservation for calendar in 2 cases (your reservation, or if admin venue all reservation)
        print("endpoint")
        out = []
        for reservation in self.get_queryset():
            out.append({
                'title': reservation.title,
                'id': reservation.id,
                'start': reservation.from_hour,
                'resourceId': reservation.track.id,
            })
        return JsonResponse(out, safe=False)
        # serializer = self.get_serializer(self.get_queryset(), many=True)
        # return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def add_reservation(self, request):
        start = self.request.GET.get("start", None)
        end = self.request.GET.get("end", None)
        title = self.request.GET.get("title", None)
        resourceId = self.request.GET.get("resourceId", None)
        venueId = self.request.GET.get("venueId", None)

        cleaned_js_start_time = start.split('(')[0].strip()
        cleaned_js_end_time = end.split('(')[0].strip()
        # Sparsowanie czasu do obiektu datetime
        dt_start = datetime.strptime(cleaned_js_start_time, "%a %b %d %Y %H:%M:%S GMT%z")
        dt_end = datetime.strptime(cleaned_js_end_time, "%a %b %d %Y %H:%M:%S GMT%z")

        # Sformatowanie czasu do YYYY-MM-DD HH:MM
        formatted_dt_start = dt_start.strftime("%Y-%m-%d %H:%M:%S")
        formatted_dt_end = dt_end.strftime("%Y-%m-%d %H:%M:%S")
        date_str, time_str = formatted_dt_start.split(" ")

        venue = Venue.objects.get(id=venueId)
        track = VenueTrack.objects.get(id=resourceId)

        event = Reservation(title=str(title), from_hour=formatted_dt_start, to_hour=formatted_dt_end,
                            creator=request.user, venue=venue, reservation_date=date_str, track=track)

        # ToDo How to add that? First create defult venue for club
        # venue

        event.save()
        data = {}
        return JsonResponse(data)

    @action(detail=False, methods=['GET'])
    def resize_reservation(self, request):
        reservation_id = self.request.GET.get("reservation_id", None)
        reservation_venue = self.request.GET.get("venueId", None)
        reservation_end = self.request.GET.get("end", None)

        reservation_end_iso = datetime.fromisoformat(reservation_end)
        reservation_end_formatted = reservation_end_iso.strftime("%Y-%m-%d %H:%M:%S")

        resized_reservation = Reservation.objects.get(id=reservation_id, venue=reservation_venue)
        resized_reservation.to_hour = reservation_end_formatted
        resized_reservation.save()

        return Response(True)

    @action(detail=False, methods=['GET'])
    def drop_reservation(self, request):
        print("HEHEHEHE")
        reservation_id = self.request.GET.get("reservation_id", None)
        reservation_venue = self.request.GET.get("venueId", None)
        reservation_start = self.request.GET.get("start", None)
        reservation_end = self.request.GET.get("end", None)
        resource_id = self.request.GET.get("resourceId", None)

        print(resource_id)

        # Remove timezone info
        reservation_start = reservation_start.split('(')[0].strip()
        reservation_end = reservation_end.split('(')[0].strip()

        # Parse the date string
        parsed_start = datetime.strptime(reservation_start, "%a %b %d %Y %H:%M:%S GMT%z")
        reservation_end = datetime.strptime(reservation_end, "%a %b %d %Y %H:%M:%S GMT%z")

        reservation_start_formatted = parsed_start.strftime("%Y-%m-%d %H:%M:%S")
        reservation_end_formatted = reservation_end.strftime("%Y-%m-%d %H:%M:%S")

        resized_reservation = Reservation.objects.get(id=reservation_id, venue=reservation_venue)
        resized_reservation.from_hour = reservation_start_formatted
        resized_reservation.to_hour = reservation_end_formatted
        if resource_id:
            print("here")
            print(resource_id)
            track = VenueTrack.objects.get(id=resource_id, venue=reservation_venue)
            print(track)
            resized_reservation.track = track
            print(resized_reservation.track)
        resized_reservation.save()

        return Response(True)


def check(request):
    queryset = Venue.objects.all()
    return render(request, 'api/check.html', {})


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    # filter_backends = DEFAULT_FILTER_BACKENDS


class VenueTrackViewSet(viewsets.ModelViewSet):
    queryset = VenueTrack.objects.all()
    serializer_class = VenueTrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
