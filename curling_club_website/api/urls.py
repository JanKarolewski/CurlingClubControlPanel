from django.urls import path, include
from rest_framework import routers
from . import views
from .views import VenueViewSet2, Logout, ClubViewSet, ReservationViewSet

router = routers.DefaultRouter()
# router.register(r'Venue1', VenueViewSet1)
router.register(r'Venue2', VenueViewSet2)
router.register(r'Club', ClubViewSet)
router.register(r'Reservation', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test', views.check, name="check"),
    path('logout/', Logout.as_view()),
]
