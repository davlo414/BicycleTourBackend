from geopy.distance import geodesic
from django.db import models

class Location(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    country = models.CharField(max_length=2)

    def __str__(self):
        return f"({self.lon}, {self.lat})"


class POI(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    details = models.TextField(null=True, blank=True)
    image = models.URLField(null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trip(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    details = models.TextField(null=True)
    image = models.URLField(null=True)
    pois = models.ManyToManyField(POI, through="TripPOI")

    def number_of_countries(self):
        return len({poi.location.country for poi in self.pois.all() if poi.location})
    
    def distance(self):
        start_poi = TripPOI.objects.filter(trip=self, position='start').first()
        end_poi = TripPOI.objects.filter(trip=self, position='end').first()
        
        if not start_poi or not end_poi:
            return 0
        
        start_coor = (start_poi.poi.location.lat, start_poi.poi.location.lon)
        end_coor = (end_poi.poi.location.lat, end_poi.poi.location.lon)

        return int(geodesic(start_coor, end_coor).mi) if start_poi and end_poi else 0

    def __str__(self):
        return self.name


class TripPOI(models.Model):
    POSITION_CHOICES = (
        ('start', 'Start'),
        ('end', 'End')
    )

    poi = models.ForeignKey(POI, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    position = models.CharField(max_length=5, choices=POSITION_CHOICES, null=True, blank=True)

    def distance_from_start(self):
        start_poi = TripPOI.objects.filter(trip=self.trip, position='start').first()
        if not start_poi:
            return 0
        
        start_coor = (start_poi.poi.location.lat, start_poi.poi.location.lon)
        trippoi_coor = (self.poi.location.lat, self.poi.location.lon)

        return geodesic(start_coor, trippoi_coor).mi
    
    def distance_to_end(self):
        end_poi = TripPOI.objects.filter(trip=self.trip, position='end').first()
        if not end_poi:
            return 0
        
        start_coor = (end_poi.poi.location.lat, end_poi.poi.location.lon)
        trippoi_coor = (self.poi.location.lat, self.poi.location.lon)

        return geodesic(start_coor, trippoi_coor).mi
    
    def __str__(self):
        return f"{self.id}, Trip: {self.trip.name}, POI: {self.poi.name}"