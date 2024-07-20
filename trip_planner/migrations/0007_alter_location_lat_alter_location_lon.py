# Generated by Django 5.0.7 on 2024-07-17 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_planner', '0006_rename_latitude_location_lat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='location',
            name='lon',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
    ]
