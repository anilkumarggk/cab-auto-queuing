from django.conf.urls import url
from .views import RideViewSet

urlpatterns = [
    url(r'^user/ride/$', RideViewSet.as_view({'post': 'create', 'get': 'list'})),
    url(r'^driver/waiting_rides/$', RideViewSet.as_view({'get': 'unassigned_rides'})),
    url(r'^driver/ongoing_ride/$', RideViewSet.as_view({'get': 'current_driver_ride'})),
    # url(r'^$', app_urls),
]
