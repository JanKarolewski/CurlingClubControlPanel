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

from members.forms import RegisterUserForm, RegisterClubForm, ProfileForm
from members.models import Profile, Club


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

    #ToDo
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
        if method == 'put':
            # return self.put(*args, **kwargs)
            return self.post(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(MembersClubView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        # confirm user request to join at CLub
        print("confirm user request to join at CLub")
        print(self.request.GET)
        print(self.club_id)
        print(self.club_member)
        profile = Profile.objects.get(pk=self.club_member, club=self.club_id)
        profile.club_profile_status = "Profile_change"
        profile.save()
        return redirect('club-members-panel')

    def delete(self, *args, **kwargs):
        # reject user request to join to Club
        print("reject user request to join to Club")
        print(self.request.GET)
        print(self.club_id)
        profile = Profile.objects.get(pk=self.club_member, club=self.club_id)
        profile.club_profile_status = "No_club_member"
        profile.club = None
        profile.save()
        return redirect('club-members-panel')


class ClubViewv2(View):
    model = Club

    def get(self, request, *args, **kwargs):
        test = request.GET.get('test')
        club = request.user.profile.club.id
        club_info = Club.objects.get(pk=club)

        return render(request, 'club/administration/club_basic_admin_panel.html', {
            'club_info': club_info
        })

    def post(self, request):
        return render(request, 'club/administration/club_basic_admin_panel.html', {})