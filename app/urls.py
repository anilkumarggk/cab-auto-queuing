from django.conf.urls import url
from .views import UserViewSet

urlpatterns = [
    url(r'^user/ride/$', UserViewSet.as_view({'post': 'create', 'get': 'list'})),
    # url(r'^$', app_urls),
]
