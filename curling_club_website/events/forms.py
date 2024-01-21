from django import forms
from django.forms import ModelForm
from . models import Venue, Event


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__"
        fields = ('name', 'address', 'phone', 'email_adress', 'zip_code')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'adress'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'web'}),
            'email_adress': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email_adress'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip_code'}),
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        # fields = "__all__"
        fields = ('name', 'event_date', 'venue', 'manager', 'description', 'attendees')
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'venue',
            'manager': 'manager',
            'description': 'description',
            'attendees': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Eventa name'}),
            'event_date': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'form-control', 'placeholder': 'event date MM/DD/YYYY'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'manager'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'description', 'rows': "4", 'cols': "50"}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
        }
