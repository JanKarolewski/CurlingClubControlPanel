# Generated by Django 4.2.7 on 2024-02-19 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_venue_administrator'),
        ('members', '0013_reservation_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenueIceOpenHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], unique=True)),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='club', to='events.venue')),
            ],
            options={
                'verbose_name_plural': 'Venue Ice Open Hours',
                'ordering': ('weekday', 'from_hour'),
                'unique_together': {('weekday', 'from_hour', 'to_hour')},
            },
        ),
        migrations.DeleteModel(
            name='ClubIceOpenHours',
        ),
    ]
