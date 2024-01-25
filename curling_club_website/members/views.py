from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
            club = club.save()
            messages.success(request, "Poprawna rejestracja klubu")
            return redirect('home')
        else:
            messages.error(request, "Błędna rejestracja klubu")
    else:
        form = RegisterClubForm()
    return render(request, 'authenticate/register_club.html', {
        'form': form,
    })


@login_required
def profile_panel(request):
    print("nowe gówno")
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


def club_info_panel(request, club_id):
    print(club_id)
    club = Club.objects.filter(id=club_id).first()
    print((club))
    print((club.phone_number))
    if club:
        return render(request, 'club/club_info_panel.html', {'club': club})
    else:
        all_clubs = Club.objects.all()
        print(all_clubs)
        return render(request, 'club/clubs_all_list.html', {'all_clubs': all_clubs})
