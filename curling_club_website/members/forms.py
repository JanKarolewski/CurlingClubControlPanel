from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms

from members.models import Club, UserApp


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(widget=forms.EmailInput())
    phone_number = PhoneNumberField(
        # toDo How?
        # widget=PhoneNumberPrefixWidget(initial='PL')
    )

    club_id = forms.ModelChoiceField(queryset=Club.objects.all(), empty_label="wybierz klub")

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'club_id', 'password1')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['club_id'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class RegisterClubForm(ModelForm):
    class Meta:
        model = Club
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RegisterClubForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['short_name'].widget.attrs['class'] = 'form-control'
        self.fields['team_short_name'].widget.attrs['class'] = 'form-control'
        self.fields['web_page'].widget.attrs['class'] = 'form-control'
        self.fields['facebook_page'].widget.attrs['class'] = 'form-control'
        self.fields['istagram_page'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['main_photo'].widget.attrs['class'] = 'form-control'

