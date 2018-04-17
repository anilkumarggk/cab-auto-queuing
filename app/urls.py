from django.conf.urls import url
from .views import UserViewSet

urlpatterns = [
    url(r'^request_ride/$', UserViewSet.as_view({'post': 'create'})),
    # url(r'^$', app_urls),
]
