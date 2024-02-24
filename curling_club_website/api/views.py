from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from members.models import Club, Reservation
from .serializers import VenueSerializer, ClubSerializer, ReservationSerializer
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
        self.queryset = self.queryset.filter(club=self.request.user.profile.club)
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        if start:
            start = datetime.strptime(start, "%Y-%m-%d")
            self.queryset = self.queryset.filter(reservation_date__gte=start)
        if end:
            end = datetime.strptime(end, "%Y-%m-%d")
            self.queryset = self.queryset.filter(reservation_date__lte=end)
        return self.queryset

    @action(detail=False, methods=['GET'])
    def reservation_for_calendar(self, request):
        # Get all club reservation for calendar
        print("endpoint")
        out = []
        for reservation in self.get_queryset():
            out.append({
                'title': reservation.title,
                'id': reservation.id,
                'start': reservation.from_hour,
                'end': reservation.to_hour,
                # toDo resourceId in reservation
                'resourceId': 'room101',
            })
        return JsonResponse(out, safe=False)
        # serializer = self.get_serializer(self.get_queryset(), many=True)
        # return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def add_reservation(self, request):
        start = self.request.GET.get("start", None)
        end = self.request.GET.get("end", None)
        title = self.request.GET.get("title", None)
        event = Reservation(title=str(title), from_hour=start, to_hour=end, creator=request.user,
                            club=self.request.user.profile.club)

        # ToDo How to add that? First create defult venue for club
        # venue

        event.save()
        data = {}
        return JsonResponse(data)


def check(request):
    queryset = Venue.objects.all()
    return render(request, 'api/check.html', {})


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    # filter_backends = DEFAULT_FILTER_BACKENDS

