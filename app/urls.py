from django.conf.urls import url
from .views import RideViewSet

urlpatterns = [
    url(r'^user/ride/$', RideViewSet.as_view({'post': 'create', 'get': 'user_rides'})),
    url(r'^driver/completed_rides/$', RideViewSet.as_view({'get': 'completed_rides'})),
    url(r'^driver/waiting_rides/$', RideViewSet.as_view({'get': 'unassigned_rides'})),
    url(r'^driver/ongoing_ride/$', RideViewSet.as_view({'get': 'current_driver_ride'})),
    url(r'^driver/pickup/$', RideViewSet.as_view({'post': 'pickup_ride'})),
    url(r'^dashboard/$', RideViewSet.as_view({'get': 'list'})),
]
