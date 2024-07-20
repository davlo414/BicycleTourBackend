from rest_framework import serializers
from trip_planner.models import Trip, POI, TripPOI, Location
from trip_planner.iso_country_codes import CC


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = CC.get(representation.get('country'))
        return representation


class POISerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = POI
        fields = '__all__'

    def create(self, validated_data):
        location = Location.objects.create(**validated_data.pop('location'))
        poi = POI.objects.create(location=location, **validated_data)
        return poi


class TripPOISerializer(serializers.ModelSerializer):
    poi = POISerializer()
    distance_from_start = serializers.FloatField(read_only=True)
    distance_to_end = serializers.FloatField(read_only=True)

    class Meta:
        model = TripPOI
        fields = '__all__'

    def create(self, validated_data):
        poi_serializer = POISerializer(data=validated_data.pop('poi'))
        poi_serializer.is_valid()
        poi = poi_serializer.save()
        trip = validated_data.pop('trip')
        trippoi = TripPOI.objects.create(poi=poi, trip=trip, **validated_data)
        return trippoi


class TripSerializer(serializers.ModelSerializer):
    pois = TripPOISerializer(source='trippoi_set', many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = '__all__'