from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from members.forms import RegisterUserForm, RegisterClubForm


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
            user = authenticate(username=username, password=password,
                                # last_name=last_name, phone_number=phone_number
                                )
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
            form.save()
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
