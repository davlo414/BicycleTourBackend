from collections import defaultdict
from operator import itemgetter

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trip_planner.serializers import TripSerializer, TripPOISerializer, POISerializer
from trip_planner.models import Trip, TripPOI, POI
from trip_planner.iso_country_codes import CC


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class POIViewSet(viewsets.ModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer


class TripPOIViewSet(viewsets.ModelViewSet):
    queryset = TripPOI.objects.all()
    serializer_class = TripPOISerializer


class POISGroupByCountry(APIView):
    def get(self, request, trip_id):
        trip_pois = TripPOI.objects.select_related("poi__location").filter(trip=trip_id)

        grouped_pois = defaultdict(list)

        for trip_poi in trip_pois:
            country_code = trip_poi.poi.location.country
            country_name = CC.get(country_code)
            grouped_pois[country_name].append(TripPOISerializer(trip_poi).data)

        for country, trippois in grouped_pois.items():
            grouped_pois[country] = sorted(trippois, key=itemgetter('distance_from_start'))

        country_avg_distance = [
            {
                'country': country,
                'avg_distance': sum(trippoi.get('distance_from_start') for trippoi in trippois) / len(trippois)
            }
            for country, trippois in grouped_pois.items()
        ]

        country_avg_distance = sorted(country_avg_distance, key=itemgetter('avg_distance'))

        return_list = [
            {"country": country_dict['country'], "data": grouped_pois[country_dict['country']]} for country_dict in country_avg_distance
        ]

        return Response(return_list)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class SetTripPOIPosition(APIView):
    def post(self, request, trippoi_id):
        trippoi = TripPOI.objects.get(id=trippoi_id)
        position = request.data.get('position')
        TripPOI.objects.filter(trip=trippoi.trip, position=position).update(position=None)
        trippoi.position = position
        trippoi.save()

        return Response()