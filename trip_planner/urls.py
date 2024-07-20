from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trip_planner import views

router = DefaultRouter()
router.register(r'trips', views.TripViewSet, basename='trip')
router.register(r'pois', views.POIViewSet, basename='poi')
router.register(r'trippois', views.TripPOIViewSet, basename='trippoi')

urlpatterns = [
    path('', include(router.urls)),
    path('pois-group-by-country/<int:trip_id>', views.POISGroupByCountry.as_view(), name='pois-group-by-country'),
    path('trippois/<int:trippoi_id>/set_position', views.SetTripPOIPosition.as_view(), name='set-trip-poi-position')
]