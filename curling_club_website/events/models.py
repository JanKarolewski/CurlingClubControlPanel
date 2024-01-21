from django.db import models
from members.models import Profile


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=120, blank=True)
    zip_code = models.CharField(max_length=120, blank=True)
    phone = models.CharField('Phone', max_length=10)
    web = models.URLField('URL Adress', blank=True)
    email_adress = models.EmailField('Email', max_length=120)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120, null=True)
    event_date = models.DateTimeField('Event Date', null=True)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='manager')
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(Profile, blank=True, related_name='attendees')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tags = models.CharField(max_length=255, default="Post")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    main_photo = models.ImageField(blank=True, null=True, upload_to='uploads/', default='uploads/OIP.jpg')

    def __str__(self):
        return self.title + " | " + str(self.author)
