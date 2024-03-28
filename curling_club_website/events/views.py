from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue, Post
from django.http import HttpResponseRedirect
from .forms import VenueForm, EventForm
from django.contrib.auth.models import Group


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    # convert for calendar
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # data
    now = datetime.now()
    current_year = now.year
    # czas
    time = now.strftime('%H:%M')

    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    return render(request,
                  'events/home.html',
                  dict(nowyear=year, month=month, month_number=month_number, cal=cal, current_year=current_year,
                       now=now, time=time))


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/event_list.html',
                  {'event_list': event_list})


def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.instance.administrator = request.user
            form.save()
            group = Group.objects.get(name="Venue admin")
            request.user.add(group)
            #toDo sprawdź czy działa, ogarnij czy to coś przez przypadek nie wywala a powinno
            request.user.venue_employee = form
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


class AllPostsListView(ListView):
    model = Post
    template_name = 'post/all_posts_list.html'


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'post/detail-post_article.html'
