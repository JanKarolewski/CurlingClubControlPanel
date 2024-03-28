from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from events.models import Venue


class Club(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    team_short_name = models.CharField(max_length=255, null=True, blank=True)
    web_page = models.URLField(max_length=255, null=True, blank=True)
    facebook_page = models.URLField(max_length=255, null=True, blank=True)
    istagram_page = models.URLField(max_length=255, null=True, blank=True)
    phone_number = phone_number = PhoneNumberField()
    main_photo = models.ImageField(blank=True, null=True, upload_to='clubs_main_photo/', default='uploads/OIP.jpg')
    club_admin = models.OneToOneField(User, on_delete=models.PROTECT, default=None)
    club_members = models.ManyToManyField(User, blank=True, null=True, related_name='club_members')

    # Todo create Adress model and add it to forms
    # adress = Adress()

    def __str__(self):
        return self.short_name


class Profile(models.Model):
    profile_status_choices = [
        ("No_club_member", "No club member"),  # to jest bez sensu, wystarczy że poleclub będzie None
        ("User_sent_join_request", "User sent join request to Club"),
        ("Profile_change", "Profile change"),
        ("Confirmed_profile", "Confirmed profile"),
        ("Profile_rejected", "Profile rejected")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.CASCADE)
    photo_profile = models.ImageField(blank=True, null=True, upload_to='user_photo_profile/', default='uploads/OIP.jpg')
    club_profile_status = models.CharField(choices=profile_status_choices, blank=True, null=True,
                                           default="No_club_member", max_length=100)
    venue_employee = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name='Venue_emplyee')

    # # ToDo special_ID code in profile
    # ID_special_indywidual_code = (...)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # this method to update profile when user is updated
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.user.username) + " | " + str(self.club)


class VenueIceOpenHours(models.Model):
    WEEKDAYS = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    ]

    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE, related_name='venue')
    weekday = models.IntegerField(choices=WEEKDAYS, unique=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        verbose_name_plural = "Venue Ice Open Hours"
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)

    def __str__(self):
        return str(self.WEEKDAYS[self.weekday - 1][1]) + " | " + str(self.venue)

    @property
    def day_week_name(self):
        return str(self.WEEKDAYS[self.weekday - 1][1])

    @property
    def day_week_number(self):
        return int(self.WEEKDAYS[self.weekday - 1][0])


class VenueTrack(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, null=True, max_length=10, default="Track 1")
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.SET_NULL, related_name='Resources_venue')

    def __str__(self):
        return str(self.venue) + " | " + str(self.title)

    @receiver(post_save, sender=Venue)
    def create_default_track(sender, instance, created, **kwargs):
        if created:
            VenueTrack.objects.create(venue=instance)


class Reservation(models.Model):
    # rezerwacja ma zawierać:
    # auto ID
    # administratora rezerwacji -> usera, który tę rezerwację założył
    # osoby, które uczestniczą w tej rezerwacji
    # datę rezerwacji
    # godzinę od
    # godzinę do
    # miejsce rezerwacji/ lodowisko -> venue
    # status = Potwierdzona, Zgłoszona, Rozliczona,

    class Status(models.TextChoices):
        Waiting_for_confirmation = "1", "Waiting for confirmation"
        Confirmed = "2", "Confirmed"
        Canceled = "3", "Canceled"
        Settled = "4", "Settled"

    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, null=True, max_length=25)
    note = models.CharField(blank=True, null=True, max_length=255)
    track = models.ForeignKey(VenueTrack, on_delete=models.CASCADE, related_name='Reservation_track', default="")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, blank=True, null=True, related_name='attendees')
    from_hour = models.DateTimeField(blank=True, null=True)
    to_hour = models.DateTimeField(blank=True, null=True)
    reservation_date = models.DateField(blank=True, null=True)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.SET_NULL, related_name='Reservation_venue')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Waiting_for_confirmation)

    def __str__(self):
        return str(self.title) + " | " + str(self.creator) + " | " + str(self.status)

    @property
    def default_venue_track(self):
        default_track = VenueTrack.object.filter(venue=self.venue)[0]
        return default_track
