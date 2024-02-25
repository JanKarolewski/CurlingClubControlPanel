from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from rest_framework.permissions import IsAuthenticated

import calendar
from calendar import HTMLCalendar
from datetime import datetime

from events.models import Venue
from members.forms import RegisterUserForm, RegisterClubForm, ProfileForm, VenueIceOpenHoursForm, VenueTrackForm
from members.models import Profile, Club, VenueIceOpenHours, Reservation, VenueTrack


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.error(request, "Correct login data...")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad login data...")
            return redirect('login')

    return render(request, 'authenticate/login.html', {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Wylogowano ze strony...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Poprawna rejestracja")
            return redirect('home')
        else:
            messages.error(request, "Błędna rejestracja")
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })


@login_required
def register_club(request):
    if request.method == 'POST':
        form = RegisterClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.club_admin = request.user
            profile = Profile.objects.get(user=request.user)
            try:
                profile.club = form.instance
                profile.save()
                messages.success(request, "Poprawna rejestracja klubu")
                return redirect('home')
            except IntegrityError:
                messages.error(request, "Brak możliwości rejestracji klubu")

        else:
            messages.error(request, "Błędna rejestracja klubu")
    else:
        form = RegisterClubForm()
    return render(request, 'authenticate/register_club.html', {
        'form': form,
    })


@login_required
def profile_panel(request):
    return render(request, 'authenticate/profile_panel.html')


@login_required
def update_user(request):
    if request.user.is_authenticated:
        user_data = User.objects.get(id=request.user.id)
        form = RegisterUserForm(request.POST or None, instance=user_data)
        if form.is_valid():
            form.save()
            login(request, user_data)
            messages.success(request, "Zaktualizowano dane")
            return redirect('home')
        return render(request, 'authenticate/update_user.html', {'form': form})
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


@login_required
def update_profile(request):
    if request.user.is_authenticated:
        user_data = User.objects.get(id=request.user.id)
        profile_data = Profile.objects.get(user=user_data)
        form = ProfileForm(request.POST or None, instance=profile_data)
        if form.is_valid():
            form.save()
            login(request, user_data)
            messages.success(request, "Zaktualizowano dane")
            return redirect('home')
        return render(request, 'authenticate/update_profile.html', {'form': form})
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


def club_info_panel(request, club):
    club = Club.objects.filter(id=club).first()
    if club:
        return render(request, 'club/club_info_panel.html', {'club': club})
    else:
        all_clubs = Club.objects.all()
        return render(request, 'club/clubs_all_list.html', {'all_clubs': all_clubs})


class ClubView(DetailView):
    model = Club
    context_object_name = 'club'
    template_name = 'club/administration/club_basic_admin_panel.html'

    # ToDo
    # permission_required = '(only_user_in_admin_club_group, only_my_club, only_login)' PermissionRequiredMixin

    # def get_context_data(self, *args, **kwargs):
    #     if self.kwargs['pk'] != self.request.user.profile.club.id:
    #         print("dupa")
    #     context = super(ClubView, self).get_context_data(*args, **kwargs)
    #     club_test = get_object_or_404(Club, id=self.kwargs['pk'])
    #     context["club_test"] = club_test
    #     return context

    def get_object(self, *args, **kwargs):
        obj = Club.objects.get(id=self.request.user.profile.club.id)
        print(obj)
        return obj


class MembersClubView(ListView):
    model = Profile
    context_object_name = 'members_list'
    template_name = 'club/administration/club_members_list.html'
    club_id = None
    club_member = None

    def get_queryset(self):
        qs_club_member = super().get_queryset().filter(club=self.club_id)
        print(qs_club_member)
        return qs_club_member

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        self.club_id = self.request.user.profile.club.id
        self.club_member = self.request.GET.get('id', False)
        if method == 'post':
            return self.post(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(MembersClubView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        # confirm user request to join at CLub
        profile = Profile.objects.get(pk=self.club_member, club=self.club_id)
        profile.club_profile_status = "Profile_change"
        profile.save()
        return redirect('club-members-panel')

    def delete(self, *args, **kwargs):
        # reject user request to join to Club
        profile = Profile.objects.get(pk=self.club_member, club=self.club_id)
        profile.club_profile_status = "No_club_member"
        profile.club = None
        profile.save()
        return redirect('club-members-panel')


def venue_info_panel(request):
    venue = Venue.objects.get(administrator=request.user)

    print(request.user.profile)

    return render(request, 'venue/venue_control_panel.html', {
        'venue': venue
    })


def venue_calendar_reservation_view(request):
    venue_ice_schedule = VenueIceOpenHours.objects.filter(venue=request.user.profile.venue)
    return render(request, 'venue/ice_reservation/venue_reseravion_control_panel.html',
                  {'venue_ice_schedule': venue_ice_schedule})


def edit_ice_availability_schedule(request, day_name):
    if request.user.is_authenticated:
        venue_ice_open_hours = VenueIceOpenHours.objects.get(venue=request.user.profile.venue, weekday=day_name)
        form = VenueIceOpenHoursForm(request.POST or None, instance=venue_ice_open_hours)
        if form.is_valid():
            form.save()
            messages.success(request, "Zaktualizowano dane o dostępności lodu")
            return redirect('venue-calendar-reservation-view')
        return render(request, 'venue/ice_reservation/edit_venue_ice_availability_schedule.html',
                      {'form': form, 'day_name': day_name})
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


def delete_ice_availability_schedule(request, day_name):
    if request.user.is_authenticated:
        venue_ice_open_hours = VenueIceOpenHours.objects.get(venue=request.user.profile.venue, weekday=day_name)
        venue_ice_open_hours.delete()
        messages.success(request, "Wykreślono dane o dostępności lodu")
        return redirect('venue-calendar-reservation-view')
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


def venue_ice_availability_schedule(request):
    if request.user.is_authenticated:
        user_venue = request.user.profile.venue
        form = VenueIceOpenHoursForm(request.POST or None)
        if form.is_valid():
            form.instance.venue = user_venue
            form.save()
            messages.success(request, "Zaktualizowano dane o dostępności lodu")
            return redirect('venue-calendar-reservation-view')
        return render(request, 'venue/ice_reservation/venue_ice_availability_schedule.html', {'form': form})
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


def create_ice_reservation_for_user(request, venue_id, day=datetime.now().day, month=datetime.now().month,
                                    year=datetime.now().year):
    # /create-ice-reservation-for-user/?year:2028/month:5/
    print(venue_id)
    venue = Venue.objects.get(id=venue_id)
    return render(request, 'venue/ice_reservation/create_ice_reservation_for_user.html',
                  {'venue': venue})


########################### VENUE TRACK ###########################
def venue_tracks_view(request):
    venue = request.user.profile.venue
    venue_track_data = VenueTrack.objects.filter(venue=venue)
    return render(request, 'venue/track_admin/venue_tracks_view.html', {'venue': venue,
                                                                        'venue_track_data': venue_track_data})


def venue_track_form(request):
    if request.user.is_authenticated:
        user_venue = request.user.profile.venue
        form = VenueTrackForm(request.POST or None)
        if form.is_valid() and user_venue:
            form.instance.venue = user_venue
            form.save()
            messages.success(request, "Zaktualizowano dane torze")
            return redirect('venue-tracks-view')
        return render(request, 'venue/track_admin/venue_tracks_information.html', {'form': form})
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


def all_venues_list(request):
    venues = Venue.objects.values('name', 'address', 'id')
    return render(request, 'venue/all_venue_list.html', {'venues': venues})


def edit_venue_track(request, track_id):
    if request.user.is_authenticated:
        venue_track_form_info = VenueTrack.objects.get(venue=request.user.profile.venue, id=track_id)
        form = VenueTrackForm(request.POST or None, instance=venue_track_form_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Zaktualizowano dane o torze")
            return redirect('venue-tracks-view')
        return render(request, 'venue/track_admin/edit_venue_tracks_information.html',
                      {'form': form, 'track_id': track_id})
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')


def delete_venue_track(request, track_id):
    if request.user.is_authenticated:
        venue_track_query = VenueTrack.objects.filter(venue=request.user.profile.venue)
        if venue_track_query.count() > 1:
            venue_track_to_delete = venue_track_query.get(id=track_id)
            venue_track_to_delete.delete()
            messages.success(request, "Wykreślono dane o torze")
            return redirect('venue-tracks-view')
        else:
            messages.error(request, "Nie można usunąć jedynego toru")
            return redirect('venue-tracks-view')
    else:
        messages.error(request, "Musisz być zalogowanym")
        return redirect('home')