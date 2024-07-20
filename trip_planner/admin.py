from django.contrib import admin

from .models import Trip, TripPOI, POI, Location

admin.site.register([Trip, TripPOI, POI, Location])