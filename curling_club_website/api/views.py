from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . serializers import VenueSerializer
from events.models import Venue


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


def check(request):
    queryset = Venue.objects.all()
    print(queryset)
    return render(request, 'api/check.html', {})
