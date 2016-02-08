from django.conf.urls import include, url
from common import views as common_views


urlpatterns = [
    url(r'^$', common_views.home, name='home'),
    url(r'^auth/', include('keystone_auth.urls', namespace='keystone_auth')),
    url(r'^ads_monitor/', include('ads_monitor.urls', namespace='ads_monitor')),
    url(r'^demoshop/', include('demoshop.urls'), namespace='demoshop'),
]
