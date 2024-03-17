# Generated by Django 4.2.7 on 2024-03-09 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_venue_employees'),
        ('members', '0023_remove_profile_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='venue_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Venue_emplyee', to='events.venue'),
        ),
    ]
