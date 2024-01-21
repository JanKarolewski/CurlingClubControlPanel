from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Club(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    team_short_name = models.CharField(max_length=255, null=True, blank=True)
    web_page = models.URLField(max_length=255, null=True, blank=True)
    facebook_page = models.URLField(max_length=255, null=True, blank=True)
    istagram_page = models.URLField(max_length=255, null=True, blank=True)
    phone_number = phone_number = PhoneNumberField()
    main_photo = models.ImageField(blank=True, null=True, upload_to='clubs_main_photo/', default='uploads/OIP.jpg')

    # Todo create Adress model and add it to forms
    # adress = Adress()

    def __str__(self):
        return self.short_name


class UserApp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    club_id = models.ForeignKey(Club, null=True, blank=True, on_delete=models.CASCADE)
    photo_profile = models.ImageField(blank=True, null=True, upload_to='user_photo_profile/', default='uploads/OIP.jpg')

    class Meta:
        managed = False
        db_table = 'userapp'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # this method to update profile when user is updated
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
