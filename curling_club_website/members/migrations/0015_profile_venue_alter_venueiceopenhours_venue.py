# Generated by Django 4.2.7 on 2024-02-19 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_venue_administrator'),
        ('members', '0014_venueiceopenhours_delete_clubiceopenhours'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.venue'),
        ),
        migrations.AlterField(
            model_name='venueiceopenhours',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venue', to='events.venue'),
        ),
    ]
