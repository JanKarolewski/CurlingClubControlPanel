from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms

from members.models import Club, Profile, VenueIceOpenHours, VenueTrack, Reservation


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(widget=forms.EmailInput())

    # club = forms.ModelChoiceField(queryset=Club.objects.all(), empty_label="wybierz klub")

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class RegisterClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'short_name', 'team_short_name', 'web_page', 'facebook_page', 'istagram_page',
                  'phone_number', 'main_photo')

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


class UploadFileWithMembersForm(forms.Form):
    # file = forms.FileField()
    # file = forms.FileField(validators=[FileExtensionValidator(['pdf', 'php', 'jpeg', 'jpg', 'png', 'txt'])])
    file = forms.FileField(validators=[FileExtensionValidator(['jpeg'])])


class ProfileForm(ModelForm):
    club = forms.ModelChoiceField(queryset=Club.objects.all(), empty_label="wybierz klub")
    phone_number = PhoneNumberField()

    class Meta:
        model = Profile
        fields = ('club', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['club'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'


class VenueIceOpenHoursForm(ModelForm):

    class Meta:
        model = VenueIceOpenHours
        fields = ('weekday', 'from_hour', 'to_hour')

        widgets = {
            'from_hour': forms.TimeInput(attrs={'type': 'time'}),
            'to_hour': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(VenueIceOpenHoursForm, self).__init__(*args, **kwargs)
        self.fields['weekday'].widget.attrs['class'] = 'form-control'
        self.fields['from_hour'].widget.attrs['class'] = 'form-control'
        self.fields['to_hour'].widget.attrs['class'] = 'form-control'


class VenueTrackForm(ModelForm):

    class Meta:
        model = VenueTrack
        fields = ('title', )

    def __init__(self, *args, **kwargs):
        super(VenueTrackForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'


class AppendAttendeesToReservationForm(ModelForm):
    # attendees = forms.ModelMultipleChoiceField(required=True, queryset=Reservation.creator)

    class Meta:
        model = Reservation
        fields = ('attendees',)

    def __init__(self, current_user_friendlist,*args, **kwargs):
        super(AppendAttendeesToReservationForm, self).__init__(*args, **kwargs)
        self.fields['attendees'].widget.attrs['class'] = 'form-control'
        check = []
        test = list(current_user_friendlist)
        for user in current_user_friendlist:
            check.append(user.profile)

        self.fields['attendees'].queryset = (self.fields['attendees'].queryset.
                                             filter(profile_friends__in=check))
